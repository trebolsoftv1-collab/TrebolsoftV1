from typing import Optional
from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate

def get_client(db: Session, client_id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[Client]:
    return db.query(Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate) -> Client:
    db_client = Client(
        dni=client.dni,
        full_name=client.full_name,
        address=client.address,
        phone=client.phone,
        email=client.email,
        collector_id=client.collector_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, data: dict) -> Optional[Client]:
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    for key, value in data.items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int) -> bool:
    db_client = get_client(db, client_id)
    if not db_client:
        return False
    db.delete(db_client)
    db.commit()
    return True
