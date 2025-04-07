from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ExpenseInput(BaseModel):
    user: str
    value: float
    reason: str