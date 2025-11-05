from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True)
    full_name = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    collector_id = Column(Integer, ForeignKey("users.id"))
    
    # Geolocalización
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Foto de la vivienda
    house_photo_url = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    collector = relationship("User", back_populates="assigned_clients")
    credits = relationship("Credit", back_populates="client")

    def __repr__(self):
        return f"<Client {self.full_name}>"
