from typing import Optional
from pydantic import BaseModel
from app.models.user import RoleType

class UserBase(BaseModel):
    username: str
    full_name: str
    phone: Optional[str] = None
    zone: Optional[str] = None
    role: RoleType

class UserCreate(UserBase):
    password: str
    supervisor_id: Optional[int] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    zone: Optional[str] = None
    password: Optional[str] = None
    supervisor_id: Optional[int] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    phone: Optional[str] = None
    zone: Optional[str] = None
    supervisor_id: Optional[int] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class LoginSchema(BaseModel):
    username: str
    password: str