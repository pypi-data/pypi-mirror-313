import abc
from abc import ABC
from decimal import Decimal
import typing

from mach_client import Token


class AmountPolicy(ABC):
    __slots__ = tuple()

    @abc.abstractmethod
    def __call__(self, src_token: Token, dest_token: Token, src_balance: int) -> int:
        pass


class FixedPercentagePolicy(AmountPolicy):
    __slots__ = ("percentage",)

    def __init__(self, percentage: Decimal):
        self.percentage = Decimal(percentage)
        assert 0.0 <= percentage <= 1.0

    @typing.override
    def __call__(self, src_token: Token, dest_token: Token, src_balance: int) -> int:
        return int(src_balance * self.percentage)


max_amount_policy = FixedPercentagePolicy(Decimal(1.0))
