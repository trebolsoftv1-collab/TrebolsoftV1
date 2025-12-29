from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_active_admin
from app.models.user import User, RoleType
from app.schemas.transaction import Transaction, TransactionCreate
from app.crud.transaction import get_transaction, get_transactions, create_transaction
from app.crud.credit import get_credit as crud_get_credit
from app.crud.client import get_subordinate_collector_ids

router = APIRouter()

@router.get("/", response_model=List[Transaction])
def list_transactions(
    skip: int = 0,
    limit: int = 100,
    credit_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == RoleType.ADMIN:
        return get_transactions(db, skip=skip, limit=limit, credit_id=credit_id, start_date=start_date, end_date=end_date)
    elif current_user.role == RoleType.SUPERVISOR:
        allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
        # Agregar IDs por nombre de usuario en assigned_routes
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                allowed_ids.extend([u.id for u in extra_users])
        return get_transactions(db, skip=skip, limit=limit, credit_id=credit_id, user_ids=allowed_ids, start_date=start_date, end_date=end_date)
    else:
        return get_transactions(db, skip=skip, limit=limit, credit_id=credit_id, user_ids=[current_user.id], start_date=start_date, end_date=end_date)

@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_new_transaction(
    tx: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    # Permisos: cualquier autenticado puede crear, pero si es collector solo dentro de su scope
    # Para supervisor, dentro de sus cobradores y él mismo
    if tx.credit_id is not None:
        credit = crud_get_credit(db, tx.credit_id)
        if not credit:
            raise HTTPException(status_code=404, detail="Credit not found")
        credit_collector_id = credit.client.collector_id if credit.client else None
        if current_user.role == RoleType.COLLECTOR:
            if credit_collector_id != current_user.id:
                raise HTTPException(status_code=403, detail="Not enough permissions for this credit")
        elif current_user.role == RoleType.SUPERVISOR:
            allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
            # Agregar IDs por nombre de usuario
            if getattr(current_user, "assigned_routes", None):
                assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
                if assigned_names:
                    extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                    allowed_ids.extend([u.id for u in extra_users])
            if credit_collector_id not in allowed_ids:
                raise HTTPException(status_code=403, detail="Not enough permissions for this credit")
    try:
        return create_transaction(db, user_id=current_user.id, tx=tx)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{tx_id}", response_model=Transaction)
def read_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = get_transaction(db, tx_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    if current_user.role == RoleType.ADMIN:
        return t
    if current_user.role == RoleType.SUPERVISOR:
        allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
        # Agregar IDs por nombre de usuario
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                allowed_ids.extend([u.id for u in extra_users])
        if t.user_id not in allowed_ids:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return t
    # collector
    if t.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return t
