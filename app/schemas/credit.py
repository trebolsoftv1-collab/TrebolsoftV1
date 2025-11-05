from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.credit import CreditStatus

class CreditBase(BaseModel):
    client_id: int
    amount: float
    interest_rate: float
    term_days: int
    insurance_amount: float | None = 0

class CreditCreate(CreditBase):
    pass

class CreditUpdate(BaseModel):
    status: Optional[CreditStatus]
    remaining_amount: Optional[float]

class Credit(CreditBase):
    id: int
    total_amount: float
    remaining_amount: float
    daily_payment: float
    status: CreditStatus
    start_date: datetime
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
