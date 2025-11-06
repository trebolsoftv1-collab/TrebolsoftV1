from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Atributos compartidos para crear/actualizar items."""
    title: str
    description: Optional[str] = None
    is_active: bool = True


class ItemCreate(ItemBase):
    """Datos necesarios para crear un item."""
    pass


class ItemUpdate(ItemBase):
    """Datos que se pueden actualizar de un item."""
    title: Optional[str] = None
    is_active: Optional[bool] = None


class Item(ItemBase):
    """Item como aparece en la base de datos."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Configuración del modelo Pydantic."""
        from_attributes = True