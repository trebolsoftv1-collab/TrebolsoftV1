from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, RoleType
from app.crud import stats as crud_stats
from app.crud import client as crud_client

router = APIRouter()

@router.get("/", tags=["stats"])
def get_stats(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    user_id: Optional[int] = Query(None),
    supervisor_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Devuelve estadísticas reales filtradas por fecha y permisos de usuario.
    """
    target_user_ids = None

    # 1. Definir el alcance (Scope) según el rol
    if current_user.role == RoleType.ADMIN:
        # Admin ve todo, a menos que filtre por un usuario específico
        if user_id:
            target_user_ids = [user_id]
        elif supervisor_id:
            # Si admin filtra por supervisor, calculamos el alcance de ese supervisor
            subordinates = crud_client.get_subordinate_collector_ids(db, supervisor_id)
            target_user_ids = subordinates + [supervisor_id]
    
    elif current_user.role == RoleType.SUPERVISOR:
        # Supervisor ve: Subordinados + Él mismo
        subordinates = crud_client.get_subordinate_collector_ids(db, current_user.id)
        allowed_ids = subordinates + [current_user.id]
        
        # Si pide un usuario específico, validar que esté en su lista permitida
        if user_id:
            if user_id not in allowed_ids:
                raise HTTPException(status_code=403, detail="No tiene permiso para ver estadísticas de este usuario")
            target_user_ids = [user_id]
        else:
            target_user_ids = allowed_ids
            
    else:
        # Cobrador solo se ve a sí mismo
        target_user_ids = [current_user.id]

    return crud_stats.get_stats(
        db=db,
        start_date=start_date,
        end_date=end_date,
        user_ids=target_user_ids
    )
