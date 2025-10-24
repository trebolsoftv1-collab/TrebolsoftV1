from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_user, check_admin_or_supervisor_role
from app.schemas.transaction import Transaction, TransactionCreate
from app.crud.transaction import get_transaction, get_transactions, create_transaction

router = APIRouter()

@router.get("/", response_model=List[Transaction], dependencies=[Depends(check_admin_or_supervisor_role)])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_transactions(db, skip=skip, limit=limit)

@router.post("/", response_model=Transaction)
def create_new_transaction(tx: TransactionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return create_transaction(db, user_id=current_user.id, tx=tx)

@router.get("/{tx_id}", response_model=Transaction)
def read_transaction(tx_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    t = get_transaction(db, tx_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return t
