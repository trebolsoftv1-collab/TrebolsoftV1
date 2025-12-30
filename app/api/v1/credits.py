from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_active_supervisor, get_current_active_admin
from app.models.user import User, RoleType
from app.models.credit import CreditStatus
from app.schemas.credit import Credit, CreditCreate, CreditUpdate
from app.crud.credit import get_credit, get_credits, create_credit, update_credit, delete_credit
from app.crud import box as crud_box
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
        # Agregar IDs por nombre de usuario en assigned_routes
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                allowed_ids.extend([u.id for u in extra_users])
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
    # 1. Obtener el cliente primero para saber quién es su cobrador
    cli = crud_get_client(db, credit.client_id)
    if not cli:
        raise HTTPException(status_code=404, detail="Client not found")

    # Validar que el cliente pertenezca a un collector permitido
    if current_user.role != RoleType.ADMIN:
        allowed_ids = get_subordinate_collector_ids(db, current_user.id) + [current_user.id]
        # Agregar IDs por nombre de usuario
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                allowed_ids.extend([u.id for u in extra_users])
        if cli.collector_id not in allowed_ids:
            raise HTTPException(status_code=403, detail="Not enough permissions for client's collector")

    # --- INTEGRACIÓN CAJA: Descontar dinero del cobrador ---
    if not cli.collector_id:
        raise HTTPException(status_code=400, detail="El cliente no tiene un cobrador asignado para descontar el dinero.")

    # Buscamos la caja del cobrador dueño del cliente (cli.collector_id)
    collector_box = crud_box.get_box_by_user_id(db, cli.collector_id)
    if not collector_box:
        raise HTTPException(status_code=404, detail=f"No se encontró la caja del cobrador (ID: {cli.collector_id})")

    # Validamos fondos suficientes
    if collector_box.base_balance < credit.amount:
        raise HTTPException(
            status_code=400, 
            detail=f"Fondos insuficientes en la caja del cobrador. Disponible: {collector_box.base_balance:,.2f}"
        )

    # Ejecutamos el descuento y registramos el movimiento
    crud_box.update_box_balance(db, collector_box, -credit.amount)
    crud_box.create_movement(
        db, collector_box.id, -credit.amount, "LOAN_DISBURSEMENT", current_user.id, f"Desembolso crédito a {cli.full_name}"
    )
    # -------------------------------------------------------

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
        # Agregar IDs por nombre de usuario
        if getattr(current_user, "assigned_routes", None):
            assigned_names = [name.strip() for name in current_user.assigned_routes.split(',') if name.strip()]
            if assigned_names:
                extra_users = db.query(User.id).filter(User.username.in_(assigned_names)).all()
                allowed_ids.extend([u.id for u in extra_users])
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
