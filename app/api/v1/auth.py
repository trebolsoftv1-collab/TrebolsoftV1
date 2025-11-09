from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.core.security import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token
)
from app.crud.user import authenticate_user, create_user, get_user_by_username, get_user_by_email
from app.schemas.user import User, UserCreate
from app.models.user import User as UserModel

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User, include_in_schema=False)
def register_user():
    """Registro deshabilitado: solo admin puede crear usuarios desde /api/v1/users."""
    raise HTTPException(status_code=403, detail="Registro público deshabilitado. Solo admin puede crear usuarios.")

@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Obtener información del usuario autenticado actual."""
    return current_user