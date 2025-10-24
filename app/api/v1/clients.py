from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, check_admin_or_supervisor_role, get_current_active_user
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.crud.client import get_client, get_clients, create_client, update_client, delete_client

router = APIRouter()

@router.get("/", response_model=List[Client], dependencies=[Depends(check_admin_or_supervisor_role)])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_clients(db, skip=skip, limit=limit)

@router.post("/", response_model=Client, dependencies=[Depends(check_admin_or_supervisor_role)])
def create_new_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.get("/{client_id}", response_model=Client)
def read_client(client_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    c = get_client(db, client_id)
    if not c:
        raise HTTPException(status_code=404, detail="Client not found")
    return c

@router.patch("/{client_id}", response_model=Client, dependencies=[Depends(check_admin_or_supervisor_role)])
def patch_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    data = payload.dict(exclude_unset=True)
    updated = update_client(db, client_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated

@router.delete("/{client_id}", dependencies=[Depends(check_admin_or_supervisor_role)])
def remove_client(client_id: int, db: Session = Depends(get_db)):
    ok = delete_client(db, client_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"ok": True}
