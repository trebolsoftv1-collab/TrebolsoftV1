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
    supervisor_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    supervisor_id: Optional[int] = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
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