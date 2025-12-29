from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_active_admin, get_current_active_supervisor
from app.models.user import User, RoleType
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.crud import user as crud_user
from app.core.security import get_password_hash, verify_password

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_user)):
    """Obtiene el perfil del usuario autenticado actual."""
    return current_user


@router.get("/", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista usuarios según permisos."""
    # Admin: ve todos
    if current_user.role == RoleType.ADMIN:
        return crud_user.get_users(db, skip=skip, limit=limit)
    
    # Supervisor: ve solo sus cobradores
    elif current_user.role == RoleType.SUPERVISOR:
        all_users = crud_user.get_users(db, skip=0, limit=10000)
        
        # Buscar usuarios por nombre escrito en assigned_routes (separado por comas)
        assigned_names = []
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            
        subordinates = [u for u in all_users if u.supervisor_id == current_user.id or u.username in assigned_names]
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
    if user.role == RoleType.ADMIN and user.supervisor_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin users cannot have a supervisor"
        )
    # Verificar que el supervisor existe
    if user.supervisor_id is not None:
        supervisor = crud_user.get_user(db, user.supervisor_id)
        if not supervisor or supervisor.role not in [RoleType.ADMIN, RoleType.SUPERVISOR]:
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
    if current_user.role == RoleType.ADMIN:
        return db_user
    
    # Supervisor: ve sus subordinados
    elif current_user.role == RoleType.SUPERVISOR:
        # Verificar si el nombre del usuario está asignado
        assigned_names = []
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            
        if db_user.supervisor_id != current_user.id and db_user.id != current_user.id and db_user.username not in assigned_names:
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


@router.patch("/me/password", response_model=UserSchema)
def change_own_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permite al usuario autenticado cambiar su propia contraseña."""
    # Restricción: Los cobradores no pueden cambiar su contraseña
    if current_user.role == RoleType.COLLECTOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Los cobradores no tienen permiso para cambiar su contraseña. Contacte a su supervisor."
        )

    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual es incorrecta."
        )
    if not new_password or len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La nueva contraseña debe tener al menos 6 caracteres."
        )
    current_user.hashed_password = get_password_hash(new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
