from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema para crear una transacción
class CashTransactionCreate(BaseModel):
    type: str
    amount: float
    description: Optional[str] = None
    related_user_id: Optional[int] = None

# Esquema base para mostrar una transacción
class CashTransactionBase(BaseModel):
    id: int
    type: str
    amount: float
    description: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True

# Esquema para mostrar el saldo
class Saldo(BaseModel):
    saldo: float
