from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, check_admin_or_supervisor_role, get_current_active_user
from app.schemas.credit import Credit, CreditCreate, CreditUpdate
from app.crud.credit import get_credit, get_credits, create_credit, update_credit, delete_credit

router = APIRouter()

@router.get("/", response_model=List[Credit], dependencies=[Depends(check_admin_or_supervisor_role)])
def list_credits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_credits(db, skip=skip, limit=limit)

@router.post("/", response_model=Credit, dependencies=[Depends(check_admin_or_supervisor_role)])
def create_new_credit(credit: CreditCreate, db: Session = Depends(get_db)):
    return create_credit(db, credit)

@router.get("/{credit_id}", response_model=Credit)
def read_credit(credit_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    c = get_credit(db, credit_id)
    if not c:
        raise HTTPException(status_code=404, detail="Credit not found")
    return c

@router.patch("/{credit_id}", response_model=Credit, dependencies=[Depends(check_admin_or_supervisor_role)])
def patch_credit(credit_id: int, payload: CreditUpdate, db: Session = Depends(get_db)):
    data = payload.dict(exclude_unset=True)
    updated = update_credit(db, credit_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Credit not found")
    return updated

@router.delete("/{credit_id}", dependencies=[Depends(check_admin_or_supervisor_role)])
def remove_credit(credit_id: int, db: Session = Depends(get_db)):
    ok = delete_credit(db, credit_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Credit not found")
    return {"ok": True}
