from datetime import datetime
from pydantic import BaseModel, EmailStr, computed_field
from typing import Optional

class ClientBase(BaseModel):
    dni: str  # Mantenemos por compatibilidad
    full_name: str  # Nombre completo (requerido)
    
    # Información de contacto
    phone: str  # Celular principal (requerido)
    phone2: Optional[str] = None  # Celular 2 (opcional)
    email: Optional[EmailStr] = None  # Email (opcional)
    
    # Información de ubicación
    city: Optional[str] = None  # Ciudad (opcional - puede ser None en BD)
    address: Optional[str] = None  # Dirección (opcional - puede ser None en BD)
    latitude: Optional[float] = None  # Latitud para Google Maps
    longitude: Optional[float] = None  # Longitud para Google Maps
    
    # Foto de la vivienda (opcional)
    house_photo_url: Optional[str] = None

class ClientCreate(ClientBase):
    collector_id: Optional[int] = None

class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    phone2: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    address: Optional[str] = None
    collector_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    house_photo_url: Optional[str] = None

class Client(ClientBase):
    id: int
    is_active: bool
    collector_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def google_maps_url(self) -> Optional[str]:
        """Generate Google Maps URL from coordinates."""
        if self.latitude is not None and self.longitude is not None:
            return f"https://maps.google.com/?q={self.latitude},{self.longitude}"
        return None

    class Config:
        from_attributes = True
