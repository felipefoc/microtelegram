from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Enum as SQLEnum
from ..database import Base
from enum import Enum
from datetime import datetime


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    user = Column(String, index=True)
    value = Column(DECIMAL, nullable=False)
    reason = Column(String, index=True)

