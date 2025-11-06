from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientUpdate


def get_subordinate_collector_ids(db: Session, supervisor_id: int) -> List[int]:
    """Obtiene IDs de todos los cobradores bajo un supervisor."""
    collectors = db.query(User.id).filter(
        User.supervisor_id == supervisor_id,
        User.role == "collector",
        User.is_active == True
    ).all()
    return [c.id for c in collectors]


def get_client(db: Session, client_id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.id == client_id).first()

def get_client_by_dni(db: Session, dni: str) -> Optional[Client]:
    """Obtiene un cliente por DNI."""
    return db.query(Client).filter(Client.dni == dni).first()

def get_clients(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    collector_id: Optional[int] = None,
    is_active: Optional[bool] = None
) -> list[Client]:
    """Lista clientes con filtros opcionales."""
    query = db.query(Client)
    
    if collector_id is not None:
        query = query.filter(Client.collector_id == collector_id)
    
    if is_active is not None:
        query = query.filter(Client.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate) -> Client:
    db_client = Client(
        dni=client.dni,
        full_name=client.full_name,
        phone=client.phone,
        phone2=client.phone2,
        email=client.email,
        city=client.city,
        address=client.address,
        latitude=client.latitude,
        longitude=client.longitude,
        house_photo_url=client.house_photo_url,
        collector_id=client.collector_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client: ClientUpdate) -> Optional[Client]:
    """Actualiza un cliente existente."""
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    update_data = client.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_client, field, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int) -> bool:
    """Desactiva un cliente (soft delete)."""
    db_client = get_client(db, client_id)
    if not db_client:
        return False
    db_client.is_active = False
    db.commit()
    return True
