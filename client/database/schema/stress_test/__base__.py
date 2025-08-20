from sqlalchemy.orm import DeclarativeBase

class StressTestBase(DeclarativeBase):
    """
    Base class for all models in the application.
    This class is used to create a declarative base for SQLAlchemy ORM.
    """
    __table_args__ = {'schema': 'stress_test'}


