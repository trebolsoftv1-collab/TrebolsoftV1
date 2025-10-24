from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import RoleType

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: RoleType

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class LoginSchema(BaseModel):
    username: str
    password: str