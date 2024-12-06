import argparse
import asyncio
import itertools
import logging
import typing

from mach_client import asset as token_factory, SupportedChain, MachClient

from . import aave, config, mach, utility, withdraw
from .aave.rebalance_manager import FrequentRebalanceManager
from .account_manager import AccountManager, AccountIDManager
from .mach.destination_policy import (
    CheapChainFixedSymbolPolicy,
    DestinationPolicy,
    RandomChainFixedSymbolPolicy,
    RandomChainRandomSymbolPolicy,
)


USAGE = """
First create a `config.yaml` file following the `template.config.yaml` template and fill in your private keys for eaech chain under `mach_cctt.secrets`.

cctt balances
    Display balances of all tokens on all supported chains from accounts specified in config.yaml in mach_cctt.secrets.

cctt run --source Arbitrum-USDC --destination USDC
    Perform the test using the account in the account file. 
    The first trade is made by selling the token specified by the --source argument.
    In each trade, a random chain is chosen as the destination chain and the entire balance of the source token is sold for the destination token.
    The choice of destination token is controlled by the --destination argument.
    In the next trade, the destination token becomes the new source token.
    This repeats until the program is stopped.

    Note: currently does not support trading the gas token (ETH) on any chain.

cctt aave
    Run the AAVE testing script. Constantly moves balances between the highest interest pool.
    Uses only stablecoins on a couple of low-gas chains.
"""

DESCRIPTION = "Cross chain trade test (CCTT) - test swaps between random chains"

DEFAULT_SOURCE_TOKEN = "Base-USDC"

DEFAULT_DESTINATION_POLICY = "USDC"

SOURCE_TOKEN_DESCRIPTION = f"""
The initial token to be sold in the first trade in the form of chain-SYMBOL, defaulting to {DEFAULT_SOURCE_TOKEN}.
If explicitly nulled out, ie. --source with no argument, then a random viable source token will be chosen for you.
"""

DESTINATION_POLICY_DESCRIPTION = f"""
Controls how the destination token is chosen in each trade.
If set to "random", then a completely random chain and symbol will be chosen.
If set to "fixed:SYMBOL", then a token on a random chain with the given symbol will be chosen.
If set to "cheap:SYMBOL", then the token with the given symbol on only Arbitrum or Optimism will be chosen.
Defaults to `{DEFAULT_DESTINATION_POLICY}`.
"""


async def show_balances(client: MachClient, account_manager: AccountManager) -> None:
    chains = (
        SupportedChain.ETHEREUM.value,
        SupportedChain.SOLANA.value,
        # SupportedChain.TRON.value,
    )

    accounts = map(
        lambda chain: account_manager[chain],
        chains,
    )

    balances = await asyncio.gather(
        *map(
            lambda account: client.get_token_balances(account.downcast()),
            accounts,
        )
    )

    iter = itertools.chain(*map(lambda balance: balance.items(), balances))

    print("Balances:")

    for _, chain_balances in iter:
        non_zero = [item for item in chain_balances.items() if item[1] > 0]

        if len(non_zero) == 0:
            continue

        print()

        for token, balance in non_zero:
            print(token.format_amount(balance))

    return


async def run() -> None:
    parser = argparse.ArgumentParser(
        prog="cctt",
        usage=USAGE,
        description=DESCRIPTION,
    )

    parser.add_argument(
        "command",
        choices=(
            "balances",
            "run",
            "aave",
            "withdraw",
        ),
        help="Command to perform",
        nargs=1,
        type=str,
    )

    parser.add_argument(
        "--source",
        "-s",
        default=DEFAULT_SOURCE_TOKEN,
        dest="src_token",
        help=SOURCE_TOKEN_DESCRIPTION,
        required=False,
        nargs="?",
        type=str,
    )

    parser.add_argument(
        "--destination-policy",
        "-d",
        default=DEFAULT_DESTINATION_POLICY,
        dest="destination_policy",
        help=DESTINATION_POLICY_DESCRIPTION,
        required=False,
        nargs="?",
        type=str,
    )

    arguments = parser.parse_args()

    command: str = arguments.command[0]
    assert command, "Command required"

    client = await MachClient.create()
    logger = logging.getLogger("cctt")

    account_manager = AccountManager(**config.config["secrets"])

    if command == "balances":
        await show_balances(client, account_manager)

        return

    match command:
        case "run":
            if arguments.src_token:
                src_token = token_factory.parse_from_str(arguments.src_token)
            else:
                src_token = await utility.choose_source_token(
                    client,
                    client.tokens,
                    account_manager[SupportedChain.ETHEREUM.value],
                )

            logger.info(f"Source token: {src_token}")

            assert (
                arguments.destination_policy
            ), "Destination policy must be provided to run test"

            match arguments.destination_policy.split(":"):
                case ["random"]:
                    logger.info("Destination token policy: randomize")
                    destination_policy: DestinationPolicy = (
                        RandomChainRandomSymbolPolicy(client)
                    )

                case ["fixed", token]:
                    logger.info(f"Destination token policy: fixed symbol {token}")
                    destination_policy: DestinationPolicy = (
                        RandomChainFixedSymbolPolicy(token)
                    )  # type: ignore
                case ["cheap", token]:
                    logger.info(f"Destination token policy: cheap chain {token}")
                    destination_policy: DestinationPolicy = CheapChainFixedSymbolPolicy(
                        token
                    )  # type: ignore
                case _ as arg:
                    typing.assert_never(arg)

            runner = mach.run(
                client=client,
                src_token=src_token,
                destination_policy=destination_policy,
                account_manager=account_manager,
                check_destination_gas=True,
                logger=logger,
            )

            async for _ in runner:
                pass

        case "aave":
            async for _ in aave.run(
                client=client,
                account_manager=account_manager,
                rebalance_manager=FrequentRebalanceManager(logger),
                filter_lower_rate_tokens=False,
                logger=logger,
            ):
                pass

        case "withdraw":
            recipients = AccountIDManager(**config.config["withdraw"])

            await withdraw.withdraw(
                client=client,
                account_manager=account_manager,
                recipients=recipients,
            )

        case _ as unreachable:
            typing.assert_never(unreachable)  # type: ignore


def main() -> None:
    logging.getLogger().setLevel(logging.DEBUG)

    # Silence annoying aiohttp warning about unclosed client session originating from web3's code
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)

    asyncio.run(run())


if __name__ == "__main__":
    main()
