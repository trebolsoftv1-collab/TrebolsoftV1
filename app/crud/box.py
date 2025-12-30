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
    """Obtiene la caja de un usuario específico con validación de permisos."""
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

    # Permisos (Misma lógica que ver la caja)
    if current_user.role == RoleType.ADMIN:
        pass
    elif current_user.role == RoleType.SUPERVISOR:
        target_user = crud_user.get_user(db, user_id)
        if target_user.id != current_user.id and target_user.supervisor_id != current_user.id:
             raise HTTPException(status_code=403, detail="Not authorized to view this box")
    else:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
    return crud_box.get_box_movements(db, target_box.id, skip, limit)

@router.post("/transfer", status_code=status.HTTP_200_OK)
def transfer_money(
    movement: BoxMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Supervisor transfiere dinero de su base a la base de un cobrador.
    """
    if current_user.role != RoleType.SUPERVISOR:
        raise HTTPException(status_code=403, detail="Only supervisors can transfer money")
    
    if not movement.target_user_id:
        raise HTTPException(status_code=400, detail="Target user required for transfer")

    # Validar que el destino sea subordinado
    target_user = crud_user.get_user(db, movement.target_user_id)
    if not target_user or target_user.supervisor_id != current_user.id:
        raise HTTPException(status_code=400, detail="Target user must be your subordinate")

    sup_box = crud_box.get_box_by_user_id(db, current_user.id)
    col_box = crud_box.get_box_by_user_id(db, target_user.id)

    if not sup_box or not col_box:
        raise HTTPException(status_code=404, detail="Box not found")

    if sup_box.base_balance < movement.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in supervisor base")

    # Ejecutar transferencia
    # 1. Restar de Supervisor
    crud_box.update_box_balance(db, sup_box, -movement.amount)
    crud_box.create_movement(db, sup_box.id, -movement.amount, "TRANSFER_OUT", current_user.id, f"Transfer to {target_user.username}")

    # 2. Sumar a Cobrador
    crud_box.update_box_balance(db, col_box, movement.amount)
    crud_box.create_movement(db, col_box.id, movement.amount, "TRANSFER_IN", current_user.id, f"Transfer from {current_user.username}")

    return {"message": "Transfer successful"}

@router.post("/expense", status_code=status.HTTP_200_OK)
def record_expense(
    movement: BoxMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cobrador registra un gasto (reduce su base)."""
    # Cobradores y supervisores pueden registrar gastos
    user_box = crud_box.get_box_by_user_id(db, current_user.id)
    if not user_box:
        raise HTTPException(status_code=404, detail="Box not found")

    crud_box.update_box_balance(db, user_box, -movement.amount)
    crud_box.create_movement(db, user_box.id, -movement.amount, "EXPENSE", current_user.id, movement.description)
    
    return {"message": "Expense recorded"}

@router.post("/withdraw", status_code=status.HTTP_200_OK)
def withdraw_money(
    movement: BoxMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Supervisor retira dinero de la caja del cobrador (ej. cierre del día).
    El dinero sale de la caja del cobrador y vuelve a la del supervisor.
    """
    if current_user.role != RoleType.SUPERVISOR:
        raise HTTPException(status_code=403, detail="Only supervisors can withdraw money")

    if not movement.target_user_id:
        raise HTTPException(status_code=400, detail="Target user required")

    target_user = crud_user.get_user(db, movement.target_user_id)
    if not target_user or target_user.supervisor_id != current_user.id:
        raise HTTPException(status_code=400, detail="Target user must be your subordinate")

    col_box = crud_box.get_box_by_user_id(db, target_user.id)
    sup_box = crud_box.get_box_by_user_id(db, current_user.id)

    if not col_box:
        raise HTTPException(status_code=404, detail="Collector box not found")

    # 1. Restar de Cobrador
    crud_box.update_box_balance(db, col_box, -movement.amount)
    crud_box.create_movement(db, col_box.id, -movement.amount, "WITHDRAWAL", current_user.id, f"Withdrawal by {current_user.username}")

    # 2. Sumar a Supervisor (Recuperación de base)
    crud_box.update_box_balance(db, sup_box, movement.amount)
    crud_box.create_movement(db, sup_box.id, movement.amount, "RECOVERY", current_user.id, f"Recovery from {target_user.username}")

    return {"message": "Withdrawal successful"}

@router.put("/{user_id}", response_model=BoxSchema)
def admin_update_box(
    user_id: int,
    box_update: BoxUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Admin modifica directamente la base o seguro (Correcciones)."""
    if current_user.role != RoleType.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin can manually edit boxes")
    
    box = crud_box.get_box_by_user_id(db, user_id)
    # Aquí implementarías la lógica de actualización directa si es necesario
    # Por seguridad, es mejor hacerlo vía movimientos, pero si se pide edición directa:
    if box_update.base_balance is not None:
        box.base_balance = box_update.base_balance
    if box_update.insurance_balance is not None:
        box.insurance_balance = box_update.insurance_balance
    
    db.commit()
    db.refresh(box)
    return box