import dataclasses
from decimal import Decimal

from mach_client.asset import EthereumToken

from .rebalance_manager import RebalanceAnalysis


@dataclasses.dataclass
class RebalanceEvaluation:
    rebalance_analysis: RebalanceAnalysis


@dataclasses.dataclass
class Withdraw:
    amounts: list[tuple[EthereumToken, Decimal]]


@dataclasses.dataclass
class Supply:
    amounts: list[tuple[EthereumToken, Decimal]]


@dataclasses.dataclass
class LiquidityRateError:
    tokens: list[EthereumToken]
    exception: Exception


@dataclasses.dataclass
class WithdrawError:
    token: EthereumToken
    amount: Decimal
    exception: Exception


@dataclasses.dataclass
class ConvertError:
    src_token: EthereumToken
    error: object


@dataclasses.dataclass
class SupplyError:
    token: EthereumToken
    amount: Decimal
    exception: Exception


AaveError = LiquidityRateError | WithdrawError | ConvertError | SupplyError

AaveEvent = RebalanceEvaluation | Withdraw | Supply | AaveError
