from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, RoleType
from app.schemas.box import Box as BoxSchema, BoxMovementCreate, BoxUpdate, CashCount, BoxCloseResponse, BoxMovement
from app.crud import box as crud_box
from app.crud import user as crud_user

router = APIRouter()

@router.get("/{user_id}", response_model=BoxSchema)
def get_user_box(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene la caja de un usuario especfico con validacin de permisos."""
    target_box = crud_box.get_box_by_user_id(db, user_id)
    if not target_box:
        raise HTTPException(status_code=404, detail="Box not found for this user")

    # Permisos
    if current_user.role == RoleType.ADMIN:
        pass # Admin ve todo
    elif current_user.role == RoleType.SUPERVISOR:
        # Supervisor ve la suya y la de sus subordinados
        target_user = crud_user.get_user(db, user_id)
        if target_user.id != current_user.id and target_user.supervisor_id != current_user.id:
             raise HTTPException(status_code=403, detail="Not authorized to view this box")
    else:
        # Cobrador solo ve la suya
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
    return target_box

@router.get("/{user_id}/history", response_model=List[BoxMovement])
def get_box_history(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el historial de movimientos de la caja de un usuario."""
    target_box = crud_box.get_box_by_user_id(db, user_id)
    if not target_box:
        raise HTTPException(status_code=404, detail="Box not found for this user")

    # Permisos (Misma lgica que ver la caja)
    if current_user.role == RoleType.ADMIN:
        pass
    elif current_user.role == RoleType.SUPERVISOR:
        target_user = crud_user.get_user(db, user_id)
        if target_user.id != current_user.id and target_user.supervisor_id != current_user.id:
             raise HTTPException(status_code=403, detail="Not authorized to view this box")
    else:
        # ...continúa el código...
