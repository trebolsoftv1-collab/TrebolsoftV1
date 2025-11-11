from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.crud import stats as crud_stats

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
    Devuelve estadísticas de cobranzas y clientes filtradas por fecha, usuario y supervisor.
    """
    return crud_stats.get_stats(
        db=db,
        start_date=start_date,
        end_date=end_date,
        user_id=user_id,
        supervisor_id=supervisor_id
    )
