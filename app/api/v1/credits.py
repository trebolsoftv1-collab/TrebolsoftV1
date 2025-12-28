from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_active_supervisor, get_current_active_admin
from app.models.user import User, RoleType
from app.models.credit import CreditStatus
from app.schemas.credit import Credit, CreditCreate, CreditUpdate
from app.crud.credit import get_credit, get_credits, create_credit, update_credit, delete_credit
from app.crud.client import get_subordinate_collector_ids, get_client as crud_get_client

router = APIRouter()

@router.get("/", response_model=List[Credit])
def list_credits(
    skip: int = 0,
    limit: int = 100,
    client_id: Optional[int] = None,
    status: Optional[CreditStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista créditos con visibilidad según rol."""
    if current_user.role == RoleType.ADMIN:
        return get_credits(db, skip=skip, limit=limit, client_id=client_id, status=status)
    elif current_user.role == RoleType.SUPERVISOR:
        allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
        return get_credits(
            db,
            skip=skip,
            limit=limit,
            client_id=client_id,
            collector_ids=allowed_ids,
            status=status,
        )
    else:
        return get_credits(
            db,
            skip=skip,
            limit=limit,
            client_id=client_id,
            collector_ids=[current_user.id],
            status=status,
        )

@router.post("/", response_model=Credit, status_code=status.HTTP_201_CREATED)
def create_new_credit(
    credit: CreditCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """Crea un nuevo crédito (solo admin/supervisor)."""
    # Validar que el cliente pertenezca a un collector permitido
    if current_user.role != RoleType.ADMIN:
        cli = crud_get_client(db, credit.client_id)
        if not cli:
            raise HTTPException(status_code=404, detail="Client not found")
        allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
        if cli.collector_id not in allowed_ids:
            raise HTTPException(status_code=403, detail="Not enough permissions for client's collector")
    return create_credit(db, credit)

@router.get("/{credit_id}", response_model=Credit)
def read_credit(
    credit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    c = get_credit(db, credit_id)
    if not c:
        raise HTTPException(status_code=404, detail="Credit not found")
    # Permisos por jerarquía
    if current_user.role == RoleType.ADMIN:
        return c
    collector_id = c.client.collector_id if c.client else None
    if current_user.role == RoleType.SUPERVISOR:
        allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
        if collector_id not in allowed_ids:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return c
    # collector
    if collector_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return c

@router.patch("/{credit_id}", response_model=Credit)
def patch_credit(
    credit_id: int,
    payload: CreditUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    updated = update_credit(db, credit_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Credit not found")
    return updated

@router.delete("/{credit_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_credit(
    credit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    ok = delete_credit(db, credit_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Credit not found")
    return None
