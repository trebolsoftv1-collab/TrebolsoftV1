from typing import Optional
from sqlalchemy.orm import Session
from app.models.cash_transaction import CashTransaction
from app.schemas.transaction import TransactionCreate


def get_transaction(db: Session, tx_id: int) -> Optional[CashTransaction]:
    return db.query(CashTransaction).filter(CashTransaction.id == tx_id).first()


def get_transactions(db: Session, skip: int = 0, limit: int = 100) -> list[CashTransaction]:
    return db.query(CashTransaction).offset(skip).limit(limit).all()


def create_transaction(db: Session, user_id: int, tx: TransactionCreate) -> CashTransaction:
    db_tx = CashTransaction(
        user_id=user_id,
        credit_id=tx.credit_id,
        amount=tx.amount,
        transaction_type=tx.transaction_type,
        description=tx.description
    )
    db.add(db_tx)
    # Si es pago, reducir remaining_amount en el crédito
    from app.models.credit import Credit
    if tx.credit_id:
        credit = db.query(Credit).filter(Credit.id == tx.credit_id).first()
        if credit:
            credit.remaining_amount = (credit.remaining_amount or 0) - tx.amount
            if credit.remaining_amount <= 0:
                credit.status = credit.status.__class__("completed")
    db.commit()
    db.refresh(db_tx)
    return db_tx
