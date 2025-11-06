from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.cash_transaction import TransactionType

class TransactionBase(BaseModel):
    amount: float
    transaction_type: TransactionType
    description: Optional[str] = None
    credit_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
