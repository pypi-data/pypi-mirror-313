from __future__ import annotations
import asyncio
from decimal import Decimal
import pprint
import typing
from typing import Iterable, Optional, Sequence

import async_lru
from eth_typing import ChecksumAddress
from mach_client import asset as asset_factory, chain_client as chain_client_factory
from mach_client.account import EthereumAccount, EthereumAccountID
from mach_client.asset import EthereumToken
from mach_client.chain import EthereumChain
from mach_client.chain_client import EthereumClient
from mach_client.transaction import EthereumTransaction
from web3 import Web3
from web3.contract import AsyncContract

from .. import config
from ..log import LogContextAdapter, Logger


LIQUIDITY_RATE_SCALING_FACTOR = 10**27


class Aave:
    __slots__ = ("logger", "atokens")

    async def _update_chain(self, chain: EthereumChain) -> None:
        client = typing.cast(EthereumClient, await chain_client_factory.create(chain))
        await self.update_atokens(client)

    @classmethod
    async def create(cls, chains: Iterable[EthereumChain], logger: Logger) -> Aave:
        instance = cls(logger)

        await asyncio.gather(*[instance._update_chain(chain) for chain in chains])

        return instance

    def __init__(self, logger: Logger) -> None:
        self.logger = LogContextAdapter(logger, "Aave")
        # Mapping of token to aToken
        self.atokens: dict[EthereumToken, EthereumToken] = {}

    # The tokens available for use in Aave pools
    @property
    def valid_tokens(self) -> list[EthereumToken]:
        return list(self.atokens.keys())

    def pool_addresses_provider(self, client: EthereumClient) -> AsyncContract:
        address = config.aave_pool_addresses_provider[client.chain]
        assert Web3.is_checksum_address(address)

        return client.native.eth.contract(
            address=typing.cast(ChecksumAddress, address),
            abi=config.aave_pool_addresses_provider_abi,
        )

    async def protocol_data_provider(self, client: EthereumClient) -> AsyncContract:
        pool_addresses_provider = self.pool_addresses_provider(client)

        address = await pool_addresses_provider.functions.getPoolDataProvider().call()

        return client.native.eth.contract(
            address=address,
            abi=config.aave_protocol_data_provider_abi,
        )

    async def pool(self, client: EthereumClient) -> AsyncContract:
        pool_addresses_provider = self.pool_addresses_provider(client)

        address = await pool_addresses_provider.functions.getPool().call()

        return client.native.eth.contract(
            address=address,
            abi=config.aave_pool_abi,
        )

    @async_lru.alru_cache()
    async def update_atokens(self, client: EthereumClient) -> None:
        protocol_data_provider = await self.protocol_data_provider(client)

        # Tuples (symbol, address) where the symbol is of the form "a<first 3 letters of chain name><symbol name>", ie. aArbUSDT
        raw_atokens: list[
            tuple[str, ChecksumAddress]
        ] = await protocol_data_provider.functions.getAllATokens().call()

        atokens = await asyncio.gather(
            *[
                EthereumToken.from_data(client, address, symbol, None)
                for symbol, address in raw_atokens
            ]
        )

        for atoken in atokens:
            # Aave has this weird thing with USDC where the atoken with symbol "USDC" actually represents a wrapped version
            # The "USDCn" token represents your actual USDC balance in the pool, where "n" stands for "native"
            symbol = "USDC" if atoken.symbol.endswith("USDCn") else atoken.symbol[4:]

            if not (
                token := typing.cast(
                    EthereumToken, asset_factory.try_lookup_symbol(client.chain, symbol)
                )
            ):
                self.logger.warning(f"Could not find token {client.chain}-{symbol}")
                continue

            self.atokens[token] = atoken

    async def get_atoken_balance(
        self, token: EthereumToken, account_id: EthereumAccountID
    ) -> int:
        if token not in self.atokens:
            await self.update_atokens(token.client)

        atoken = self.atokens[token]

        return await atoken.get_balance(account_id)

    async def get_atoken_balance_in_coins(
        self, token: EthereumToken, account_id: EthereumAccountID
    ) -> Decimal:
        balance = await self.get_atoken_balance(token, account_id)
        return self.atokens[token].to_coins(balance)

    async def get_liquidity_rate(self, token: EthereumToken) -> Decimal:
        pool = await self.pool(token.client)
        reserve_data = await pool.functions.getReserveData(token.address).call()
        return Decimal(reserve_data[2]) / LIQUIDITY_RATE_SCALING_FACTOR

    # Returned dict is ordered by liquidity rate, descending
    async def get_liquidity_rates(
        self,
        tokens: Sequence[EthereumToken],
    ) -> dict[EthereumToken, Decimal]:
        liquidity_rates = await asyncio.gather(*map(self.get_liquidity_rate, tokens))

        result = list(zip(tokens, liquidity_rates))
        result.sort(key=lambda x: x[1], reverse=True)

        return dict(result)

    async def supply(
        self, token: EthereumToken, account: EthereumAccount
    ) -> tuple[int, Optional[Exception]]:
        logger = LogContextAdapter(self.logger, f"{token} => Aave")

        if (balance := await token.get_balance(account.downcast())) <= 0:
            logger.warning("Balance was empty, not supplying")
            return 0, None

        try:
            pool = await self.pool(token.client)

            supply_function = pool.functions.supply(
                token.address,
                balance,
                account.address,
                0,  # Referral code
            )

            # TODO: This should be `balance`, but that causes occasional errors like this:
            # web3.exceptions.ContractLogicError: ('execution reverted: ERC20: transfer amount exceeds allowance', '0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002845524332303a207472616e7366657220616d6f756e74206578636565647320616c6c6f77616e6365000000000000000000000000000000000000000000000000')
            # Maybe you can't withdraw any additional interest accrued within the current block even if it is counted in balanceOf?
            approval_amount = config.solidity_uint_max
            spender = EthereumAccountID(token.chain, pool.address)

            logger.info(f"Approving {approval_amount} units")

            await token.approve(
                account,
                spender,
                approval_amount,
            )

            logger.info(f"Supplying {balance} units")
            transaction = await EthereumTransaction.from_contract_function(
                token.client,
                supply_function,
                account,
            )
            sent_transaction = await transaction.broadcast()
            logger.debug("Transaction sent")

            receipt = await sent_transaction.wait_for_receipt()
            logger.debug("Receipt:")
            logger.debug(pprint.pformat(receipt))

        except Exception as e:
            return balance, e

        logger.info("Supply successful")

        return balance, None

    async def withdraw(
        self, token: EthereumToken, account: EthereumAccount
    ) -> tuple[int, Optional[Exception]]:
        logger = LogContextAdapter(self.logger, f"Aave {token} => account")

        if (balance := await self.get_atoken_balance(token, account.downcast())) <= 0:
            logger.debug("Balance was empty, not withdrawing")
            return 0, None

        try:
            pool = await self.pool(token.client)

            withdraw_function = pool.functions.withdraw(
                token.address,
                config.solidity_uint_max,  # Means withdraw everything
                account.address,
            )

            logger.info(f"Withdrawing {balance} units")
            transaction = await EthereumTransaction.from_contract_function(
                token.client,
                withdraw_function,
                account,
            )
            sent_transaction = await transaction.broadcast()
            logger.debug("Transaction sent")

            receipt = await sent_transaction.wait_for_receipt()
            logger.debug("Receipt:")
            logger.debug(pprint.pformat(receipt))

        except Exception as e:
            return balance, e

        logger.info("Withdraw successful")

        return balance, None
