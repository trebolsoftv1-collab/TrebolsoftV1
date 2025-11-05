from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.cash_transaction import CashTransaction, TransactionType
from app.models.credit import Credit, CreditStatus
from app.schemas.transaction import TransactionCreate


def get_transaction(db: Session, tx_id: int) -> Optional[CashTransaction]:
    return db.query(CashTransaction).filter(CashTransaction.id == tx_id).first()


def get_transactions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    user_ids: Optional[List[int]] = None,
    credit_id: Optional[int] = None,
) -> list[CashTransaction]:
    query = db.query(CashTransaction)
    if user_ids is not None:
        if len(user_ids) == 0:
            return []
        query = query.filter(CashTransaction.user_id.in_(user_ids))
    if credit_id is not None:
        query = query.filter(CashTransaction.credit_id == credit_id)
    return query.order_by(CashTransaction.created_at.desc()).offset(skip).limit(limit).all()


def create_transaction(db: Session, user_id: int, tx: TransactionCreate) -> CashTransaction:
    """Crea una transacción y aplica efectos colaterales si corresponde (ej: pago de crédito)."""
    # Validaciones básicas
    if tx.transaction_type == TransactionType.PAYMENT:
        if not tx.credit_id:
            raise ValueError("Payment transactions require credit_id")
        credit = db.query(Credit).filter(Credit.id == tx.credit_id).first()
        if not credit:
            raise ValueError("Credit not found")
        if credit.remaining_amount is None:
            credit.remaining_amount = credit.total_amount or 0.0
        if tx.amount <= 0:
            raise ValueError("Payment amount must be positive")
        if tx.amount > credit.remaining_amount + 1e-9:
            raise ValueError("Payment amount exceeds remaining balance")

    db_tx = CashTransaction(
        user_id=user_id,
        credit_id=tx.credit_id,
        amount=tx.amount,
        transaction_type=tx.transaction_type,
        description=tx.description,
    )
    db.add(db_tx)

    # Efecto: si es pago, reducir saldo y cerrar si llega a cero
    if tx.transaction_type == TransactionType.PAYMENT and tx.credit_id:
        credit = db.query(Credit).filter(Credit.id == tx.credit_id).first()
        if credit:
            credit.remaining_amount = max(0.0, (credit.remaining_amount or 0.0) - tx.amount)
            if credit.remaining_amount == 0.0:
                credit.status = CreditStatus.COMPLETED

    db.commit()
    db.refresh(db_tx)
    return db_tx
