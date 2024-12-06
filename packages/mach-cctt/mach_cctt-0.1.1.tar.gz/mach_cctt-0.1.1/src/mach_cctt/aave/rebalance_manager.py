import abc
from abc import ABC
import dataclasses
from decimal import Decimal
import typing

from mach_client.asset import EthereumToken

from .. import config
from ..log import LogContextAdapter, Logger


@dataclasses.dataclass(kw_only=True)
class RebalanceAnalysis:
    rebalance: bool


class RebalanceManager(ABC):
    def __init__(self, logger: Logger):
        self.logger = logger

    @abc.abstractmethod
    def __call__(
        self,
        token_rates: dict[EthereumToken, Decimal],
        portfolio_balances: list[tuple[EthereumToken, Decimal]],
    ) -> RebalanceAnalysis:
        pass


class ProfitableRebalanceManager(RebalanceManager):
    def __init__(self, logger: Logger):
        super().__init__(LogContextAdapter(logger, "Profitable Rebalance Manager"))

    @dataclasses.dataclass(kw_only=True)
    class RebalanceAnalysis(RebalanceAnalysis):
        token_rates: dict[EthereumToken, Decimal]
        portfolio_interest_rate: Decimal
        portfolio_balances: list[tuple[EthereumToken, Decimal]]

    @typing.override
    def __call__(
        self,
        token_rates: dict[EthereumToken, Decimal],
        portfolio_balances: list[tuple[EthereumToken, Decimal]],
    ) -> RebalanceAnalysis:
        self.logger.info("Checking for rebalance")

        portfolio_balance = sum(map(lambda balance: balance[1], portfolio_balances))

        portfolio_interest_rate = (
            sum(
                balance * token_rates[token] / portfolio_balance
                for token, balance in portfolio_balances
            )
            if portfolio_balance > 0
            else 0
        )

        self.logger.info(f"Portfolio interest rate: {portfolio_interest_rate}")

        highest_rate = next(iter(token_rates.values()))

        return self.RebalanceAnalysis(
            rebalance=highest_rate - portfolio_interest_rate
            > config.aave_rebalance_threshold,
            token_rates=token_rates,
            portfolio_interest_rate=Decimal(portfolio_interest_rate),
            portfolio_balances=portfolio_balances,
        )


class FrequentRebalanceManager(RebalanceManager):
    def __init__(self, logger: Logger):
        super().__init__(LogContextAdapter(logger, "Frequent Rebalance Manager"))

    @dataclasses.dataclass(kw_only=True)
    class RebalanceAnalysis(RebalanceAnalysis):
        token_rates: dict[EthereumToken, Decimal]
        portfolio_balances: list[tuple[EthereumToken, Decimal]]

    @typing.override
    def __call__(
        self,
        token_rates: dict[EthereumToken, Decimal],
        portfolio_balances: list[tuple[EthereumToken, Decimal]],
    ) -> RebalanceAnalysis:
        self.logger.info("Checking for rebalance")

        return self.RebalanceAnalysis(
            rebalance=True,
            token_rates=token_rates,
            portfolio_balances=portfolio_balances,
        )
