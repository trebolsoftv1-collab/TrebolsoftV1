from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientBase(BaseModel):
    dni: str
    full_name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class ClientCreate(ClientBase):
    collector_id: Optional[int] = None

class ClientUpdate(BaseModel):
    full_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    collector_id: Optional[int]

class Client(ClientBase):
    id: int
    is_active: bool
    collector_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
