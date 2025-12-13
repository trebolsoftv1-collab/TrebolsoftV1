from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True)  # Mantenemos DNI por compatibilidad
    full_name = Column(String)  # Nombre completo
    
    # Información de contacto
    phone = Column(String)  # Celular principal
    phone2 = Column(String, nullable=True)  # Celular 2 (opcional)
    email = Column(String, nullable=True)  # Email (opcional)
    ocupacion = Column(String, nullable=True)  # Ocupación u Oficio
    
    # Información de ubicación
    city = Column(String)  # Ciudad
    address = Column(String)  # Dirección
    latitude = Column(Float, nullable=True)  # Latitud para Google Maps
    longitude = Column(Float, nullable=True)  # Longitud para Google Maps
    
    # Foto de la vivienda (opcional)
    house_photo_url = Column(String, nullable=True)
    
    # Sistema
    is_active = Column(Boolean, default=True)
    collector_id = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    collector = relationship("User", back_populates="assigned_clients")
    credits = relationship("Credit", back_populates="client")

    def __repr__(self):
        return f"<Client {self.full_name}>"
