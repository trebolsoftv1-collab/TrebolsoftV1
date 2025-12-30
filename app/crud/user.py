from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()



def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone=user.phone,
        zone=user.zone,
        role=user.role,
        supervisor_id=user.supervisor_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user