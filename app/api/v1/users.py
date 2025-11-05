from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_active_admin, get_current_active_supervisor
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate
from app.crud import user as crud_user

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista usuarios según permisos."""
    # Admin: ve todos
    if current_user.role == "admin":
        return crud_user.get_users(db, skip=skip, limit=limit)
    
    # Supervisor: ve solo sus cobradores
    elif current_user.role == "supervisor":
        all_users = crud_user.get_users(db, skip=0, limit=10000)
        subordinates = [u for u in all_users if u.supervisor_id == current_user.id]
        return subordinates[skip:skip+limit]
    
    # Cobrador: solo se ve a sí mismo
    else:
        return [current_user]


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def admin_create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Crea usuario con validación jerárquica."""
    # Solo admin puede crear usuarios
    # Validar: si crea supervisor/cobrador, puede asignar supervisor
    if user.role == "admin" and user.supervisor_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin users cannot have a supervisor"
        )
    # Verificar que el supervisor existe
    if user.supervisor_id is not None:
        supervisor = crud_user.get_user(db, user.supervisor_id)
        if not supervisor or supervisor.role not in ["admin", "supervisor"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid supervisor_id"
            )
    return crud_user.create_user(db, user)


@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene un usuario por ID."""
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Admin: acceso total
    if current_user.role == "admin":
        return db_user
    
    # Supervisor: ve sus subordinados
    elif current_user.role == "supervisor":
        if db_user.supervisor_id != current_user.id and db_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return db_user
    
    # Cobrador: solo se ve a sí mismo
    else:
        if db_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return db_user
