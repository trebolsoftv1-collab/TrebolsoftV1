from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class BoxMovementBase(BaseModel):
    amount: float
    movement_type: str
    description: Optional[str] = None
    is_insurance: bool = False

class BoxMovementCreate(BoxMovementBase):
    target_user_id: Optional[int] = None # Requerido para transferencias

class BoxMovement(BoxMovementBase):
    id: int
    box_id: int
    created_at: datetime
    performed_by_id: Optional[int]

    class Config:
        orm_mode = True

class BoxBase(BaseModel):
    base_balance: float
    insurance_balance: float

class BoxUpdate(BaseModel):
    base_balance: Optional[float] = None
    insurance_balance: Optional[float] = None

class Box(BoxBase):
    id: int
    user_id: int
    last_updated: Optional[datetime]
    # No incluimos movements por defecto para no saturar la respuesta, 
    # se pueden pedir en un endpoint de detalle si es necesario.

    class Config:
        orm_mode = True

class CashCount(BaseModel):
    bill_100000: int = 0
    bill_50000: int = 0
    bill_20000: int = 0
    bill_10000: int = 0
    bill_5000: int = 0
    bill_2000: int = 0
    coin_1000: int = 0
    coin_500: int = 0
    coin_200: int = 0
    coin_100: int = 0
    coin_50: int = 0

    @property
    def total_amount(self) -> float:
        return (
            self.bill_100000 * 100000 +
            self.bill_50000 * 50000 +
            self.bill_20000 * 20000 +
            self.bill_10000 * 10000 +
            self.bill_5000 * 5000 +
            self.bill_2000 * 2000 +
            self.coin_1000 * 1000 +
            self.coin_50 * 50
        )

class BoxCloseResponse(BaseModel):
    system_balance: float
    counted_balance: float
    difference: float
    status: str  # MATCH, SURPLUS, SHORTAGE

