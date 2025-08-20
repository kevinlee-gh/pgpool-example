from typing import List
from sqlalchemy.orm import DeclarativeBase

from .stress_test import StressTestBase

LS_SCHEMA: List[DeclarativeBase] = [
    StressTestBase,
]

__all__ = [LS_SCHEMA]
