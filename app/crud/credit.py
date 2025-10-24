from typing import Optional
from sqlalchemy.orm import Session
from app.models.credit import Credit
from app.schemas.credit import CreditCreate


def get_credit(db: Session, credit_id: int) -> Optional[Credit]:
    return db.query(Credit).filter(Credit.id == credit_id).first()


def get_credits(db: Session, skip: int = 0, limit: int = 100) -> list[Credit]:
    return db.query(Credit).offset(skip).limit(limit).all()


def create_credit(db: Session, credit: CreditCreate) -> Credit:
    # calcular pagos sencillos: total_amount y daily_payment
    total = credit.amount * (1 + credit.interest_rate / 100)
    daily = total / credit.term_days if credit.term_days else total
    db_credit = Credit(
        client_id=credit.client_id,
        amount=credit.amount,
        interest_rate=credit.interest_rate,
        term_days=credit.term_days,
        total_amount=total,
        remaining_amount=total,
        daily_payment=daily
    )
    db.add(db_credit)
    db.commit()
    db.refresh(db_credit)
    return db_credit


def update_credit(db: Session, credit_id: int, data: dict) -> Optional[Credit]:
    db_credit = get_credit(db, credit_id)
    if not db_credit:
        return None
    for key, value in data.items():
        setattr(db_credit, key, value)
    db.commit()
    db.refresh(db_credit)
    return db_credit


def delete_credit(db: Session, credit_id: int) -> bool:
    db_credit = get_credit(db, credit_id)
    if not db_credit:
        return False
    db.delete(db_credit)
    db.commit()
    return True
