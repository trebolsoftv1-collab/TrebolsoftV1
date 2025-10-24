from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, check_admin_role, get_current_active_user
from app.schemas.user import User, UserCreate
from app.crud.user import get_users, get_user, create_user

router = APIRouter()

@router.get("/", response_model=List[User], dependencies=[Depends(check_admin_role)])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=User, dependencies=[Depends(check_admin_role)])
def admin_create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
