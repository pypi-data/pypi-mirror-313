from typing import AsyncGenerator

from .aave.event import AaveEvent
from .mach.event import TestEvent


Runner = AsyncGenerator[AaveEvent | TestEvent, None]


__all__ = ["Runner"]
