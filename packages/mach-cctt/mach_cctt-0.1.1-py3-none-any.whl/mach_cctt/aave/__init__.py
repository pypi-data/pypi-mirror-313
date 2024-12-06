import asyncio
from decimal import Decimal
import itertools
import pprint
import typing
from typing import AsyncGenerator

from mach_client import MachClient, SupportedChain
from mach_client.account import EthereumAccount
from mach_client.client.event import Trade

from .. import config, mach
from ..account_manager import AccountManager
from ..mach.destination_policy import TokenIteratorPolicy
from ..log import Logger
from .aave import Aave
from .event import (
    AaveEvent,
    ConvertError,
    LiquidityRateError,
    RebalanceEvaluation,
    Supply,
    SupplyError,
    Withdraw,
    WithdrawError,
)
from .rebalance_manager import RebalanceManager


async def run(
    *,
    client: MachClient,
    account_manager: AccountManager,
    rebalance_manager: RebalanceManager,
    # When rebalancing, if swapping to higher rate tokens fails, should we try swapping to a lower rate token or keep what we have?
    filter_lower_rate_tokens: bool,
    logger: Logger,
) -> AsyncGenerator[AaveEvent, None]:
    chains = frozenset(
        (
            SupportedChain.ARBITRUM.value,
            SupportedChain.BASE.value,
            SupportedChain.OPTIMISM.value,
        )
    )

    aave = await Aave.create(chains, logger)

    tokens = [
        token for token in aave.valid_tokens if token.symbol in config.aave_symbols
    ]

    logger.info("Tokens:")
    logger.info(pprint.pformat(tokens))

    while True:
        # Inner loop determines when to rebalance portfolio
        while True:
            try:
                token_rates = await aave.get_liquidity_rates(tokens)
            except Exception as e:
                logger.error(
                    "An exception was thrown while fetching liquidity rates from Aave:",
                    exc_info=e,
                )
                yield LiquidityRateError(tokens, e)
                continue

            logger.info("Liquidity rates:")
            logger.info(pprint.pformat(token_rates))

            portfolio_balances = await asyncio.gather(
                *[
                    aave.get_atoken_balance_in_coins(
                        token,
                        typing.cast(
                            EthereumAccount, account_manager[token.chain]
                        ).downcast(),
                    )
                    for token in tokens
                ]
            )

            portfolio_balance_pairs = list(zip(tokens, portfolio_balances))

            logger.info("Portfolio balances:")
            logger.info(pprint.pformat(portfolio_balance_pairs))

            rebalance_analysis = rebalance_manager(token_rates, portfolio_balance_pairs)

            yield RebalanceEvaluation(rebalance_analysis)

            if rebalance_analysis.rebalance:
                break

            logger.info("Not rebalancing portfolio")
            await asyncio.sleep(config.aave_supply_duration)

        logger.info("Rebalancing portfolio")

        logger.info("Withdrawing funds from Aave")

        withdrawn = []

        for token in tokens:
            account = typing.cast(EthereumAccount, account_manager[token.chain])
            amount, exception = await aave.withdraw(token, account)

            if exception:
                logger.error(
                    f"An exception was thrown while withdrawing {token} from Aave:",
                    exc_info=exception,
                )
                yield WithdrawError(token, token.to_coins(amount), exception)
                continue

            elif amount <= 0:
                continue

            withdrawn.append((token, token.to_coins(amount)))

        yield Withdraw(withdrawn)

        logger.info("Swapping funds in wallet")

        for src_token, rate in token_rates.items():
            account = typing.cast(EthereumAccount, account_manager[src_token.chain])

            if await src_token.get_balance(account.downcast()) <= 0:
                continue

            if filter_lower_rate_tokens:
                next_tokens = itertools.takewhile(
                    lambda item: item[1] > rate, token_rates.items()
                )
            else:
                next_tokens = token_rates.items()

            if not next_tokens:
                continue

            destination_policy = TokenIteratorPolicy(
                client,
                map(lambda item: item[0], next_tokens),
            )

            runner = mach.run(
                client=client,
                src_token=src_token,
                destination_policy=destination_policy,
                account_manager=account_manager,
                logger=logger,
            )

            try:
                async for event in runner:
                    if isinstance(event, Trade):
                        break

                    logger.error(f"Unexpected event while swapping out of {src_token}:")
                    logger.error(pprint.pformat(event))

                    yield ConvertError(src_token, event)

            except Exception as e:
                logger.error(
                    f"An exception was thrown while swapping {src_token}:", exc_info=e
                )
                yield ConvertError(src_token, e)

        supplied = []

        for token in tokens:
            account = typing.cast(EthereumAccount, account_manager[token.chain])
            amount, exception = await aave.supply(token, account)

            if exception:
                logger.error(
                    "An exception was thrown while supplying " f"{token} to Aave:",
                    exc_info=exception,
                )
                yield SupplyError(
                    token, Decimal(amount) / 10**token.decimals, exception
                )
                continue
            elif amount <= 0:
                continue

            supplied.append((token, Decimal(amount) / 10**token.decimals))

        yield Supply(supplied)

        if not supplied:
            logger.warning("No tokens were supplied. Trying again.")
            continue

        logger.info("Sleeping...")
        await asyncio.sleep(config.aave_supply_duration)
