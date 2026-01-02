from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User as UserModel
from app.models.cash_transaction import TransactionType
from app.schemas.caja import Saldo as SaldoSchema, CashTransactionCreate, CashTransactionBase
from app.crud import crud_caja

router = APIRouter()

@router.get("/saldo", response_model=SaldoSchema)
def get_saldo_caja(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene el saldo de caja actual para el usuario autenticado.
    """
    saldo = crud_caja.get_user_balance(db, user_id=current_user.id)
    return {"saldo": saldo}

@router.get("/movimientos", response_model=List[CashTransactionBase])
def get_movimientos_caja(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtiene una lista de movimientos de caja para el usuario autenticado.
    """
    movimientos = crud_caja.get_cash_transactions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return movimientos

@router.post("/movimientos", response_model=CashTransactionBase)
def create_nuevo_movimiento_caja(
    transaction: CashTransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Crea un nuevo movimiento de caja (ingreso, egreso, etc.).
    """
    # Validar que el tipo de transacción sea válido usando el Enum del modelo
    valid_transaction_types = [item.value for item in TransactionType]
    if transaction.type not in valid_transaction_types:
        raise HTTPException(status_code=400, detail=f"Tipo de transacción no válido. Tipos permitidos: {valid_transaction_types}")

    # Si es un retiro o desembolso, verificar que haya saldo suficiente
    if transaction.type in [TransactionType.WITHDRAWAL.value, TransactionType.DISBURSEMENT.value]:
        current_balance = crud_caja.get_user_balance(db, user_id=current_user.id)
        if current_balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar la operación.")

    new_transaction = crud_caja.create_cash_transaction(db=db, transaction_data=transaction, user_id=current_user.id)
    
    if not new_transaction:
        raise HTTPException(status_code=400, detail="Error al crear la transacción.")

    return new_transaction

