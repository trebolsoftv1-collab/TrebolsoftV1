from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_active_admin
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, Item as ItemSchema

router = APIRouter()


@router.get("/items", response_model=List[ItemSchema])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos los items."""
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


@router.post("/items", response_model=ItemSchema, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    """Crea un nuevo item."""
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items/{item_id}", response_model=ItemSchema)
def read_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un item por su ID."""
    if item := db.query(Item).filter(Item.id == item_id).first():
        return item
    raise HTTPException(status_code=404, detail="Item no encontrado")


@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    """Actualiza un item."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    """Elimina un item."""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    db.delete(db_item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)