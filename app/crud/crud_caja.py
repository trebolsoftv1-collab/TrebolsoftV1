from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cash_transaction import CashTransaction, TransactionType
from app.schemas.caja import CashTransactionCreate

def get_user_balance(db: Session, user_id: int) -> float:
    """
    Calcula y devuelve el saldo de un usuario basado en las transacciones de caja.
    - Suman: Depósitos (DEPOSIT) y Pagos de clientes (PAYMENT).
    - Restan: Retiros (WITHDRAWAL) y Desembolsos de créditos (DISBURSEMENT).
    """
    total_income = db.query(func.sum(CashTransaction.amount)).filter(
        CashTransaction.user_id == user_id,
        CashTransaction.transaction_type.in_([TransactionType.DEPOSIT, TransactionType.PAYMENT])
    ).scalar() or 0.0

    total_expense = db.query(func.sum(CashTransaction.amount)).filter(
        CashTransaction.user_id == user_id,
        CashTransaction.transaction_type.in_([TransactionType.WITHDRAWAL, TransactionType.DISBURSEMENT])
    ).scalar() or 0.0

    return total_income - total_expense

def get_cash_transactions_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Obtiene las transacciones de caja para un usuario específico.
    """
    return db.query(CashTransaction).filter(CashTransaction.user_id == user_id).order_by(CashTransaction.created_at.desc()).offset(skip).limit(limit).all()

def create_cash_transaction(db: Session, transaction_data: CashTransactionCreate, user_id: int):
    """
    Crea una nueva transacción de caja para un usuario de forma segura.
    """
    # Convierte el string del tipo de transacción al Enum correspondiente
    try:
        transaction_type_enum = TransactionType(transaction_data.type)
    except ValueError:
        # Esto no debería ocurrir si la validación está en el router, pero es una salvaguarda
        return None

    db_transaction = CashTransaction(
        user_id=user_id,
        amount=transaction_data.amount,
        transaction_type=transaction_type_enum,
        description=transaction_data.description
        # related_user_id no se está usando por ahora, se puede añadir si es necesario
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
