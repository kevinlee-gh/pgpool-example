from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy import Column, BigInteger, DateTime

from .__base__ import StressTestBase

class Counter(StressTestBase):
    __tablename__ = 'counter'
    
    id: Mapped[int] = Column(BigInteger(), primary_key=True)
    value: Mapped[int] = Column(BigInteger())

    created_at: Mapped[DateTime] = Column(DateTime(), default=datetime.now())
    updated_at: Mapped[DateTime] = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())
