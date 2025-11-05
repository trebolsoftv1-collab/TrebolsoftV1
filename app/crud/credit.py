from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.credit import Credit, CreditStatus
from app.models.client import Client
from app.schemas.credit import CreditCreate, CreditUpdate


def get_credit(db: Session, credit_id: int) -> Optional[Credit]:
    return db.query(Credit).filter(Credit.id == credit_id).first()


def get_credits(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    *,
    client_id: Optional[int] = None,
    collector_ids: Optional[List[int]] = None,
    status: Optional[CreditStatus] = None,
) -> list[Credit]:
    """Lista créditos con filtros opcionales.

    - client_id: filtra por cliente
    - collector_ids: IDs de cobradores permitidos (se aplica via relación Client.collector_id)
    - status: estado del crédito
    """
    query = db.query(Credit)
    if client_id is not None:
        query = query.filter(Credit.client_id == client_id)
    if collector_ids is not None:
        if len(collector_ids) == 0:
            return []
        # Join con Client para filtrar por collector_id permitido
        query = query.join(Client, Client.id == Credit.client_id).filter(Client.collector_id.in_(collector_ids))
    if status is not None:
        query = query.filter(Credit.status == status)
    return query.offset(skip).limit(limit).all()


def create_credit(db: Session, credit: CreditCreate) -> Credit:
    # calcular pagos sencillos: total_amount y daily_payment
    insurance = float(credit.insurance_amount or 0)
    total = credit.amount * (1 + credit.interest_rate / 100) + insurance
    daily = total / credit.term_days if credit.term_days else total
    db_credit = Credit(
        client_id=credit.client_id,
        amount=credit.amount,
        interest_rate=credit.interest_rate,
        term_days=credit.term_days,
        insurance_amount=insurance,
        total_amount=total,
        remaining_amount=total,
        daily_payment=daily
    )
    db.add(db_credit)
    db.commit()
    db.refresh(db_credit)
    return db_credit


def update_credit(db: Session, credit_id: int, payload: CreditUpdate | dict) -> Optional[Credit]:
    db_credit = get_credit(db, credit_id)
    if not db_credit:
        return None
    data = payload if isinstance(payload, dict) else payload.model_dump(exclude_unset=True)
    # Validaciones y reglas de negocio
    remaining = data.get("remaining_amount")
    if remaining is not None:
        # No permitir negativos ni mayores que total
        if remaining < 0:
            remaining = 0
        if db_credit.total_amount is not None and remaining > db_credit.total_amount:
            remaining = db_credit.total_amount
        db_credit.remaining_amount = remaining
        # Actualizar estado si queda en cero
        if remaining == 0:
            db_credit.status = CreditStatus.COMPLETED
    if "status" in data and data["status"] is not None:
        db_credit.status = data["status"]
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
