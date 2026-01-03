from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
import enum

from app.core.database import Base

class RoleType(str, enum.Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    COLLECTOR = "COLLECTOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # email eliminado
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone = Column(String, nullable=True)  # Campo para celular, sin restricción unique
    zone = Column(String, nullable=True)   # Nuevo campo para zona asignada
    role = Column(Enum(RoleType))
    is_active = Column(Boolean, default=True)
    supervisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    assigned_clients = relationship("Client", back_populates="collector", cascade="all, delete-orphan")
    supervised_collectors = relationship(
        "User",
        backref=backref(
            "supervisor",
            remote_side=[id],
            foreign_keys=["supervisor_id"],
            cascade="all, delete-orphan",
            single_parent=True
        ),
        remote_side=[id],
        foreign_keys=[supervisor_id],
        cascade="all, delete-orphan",
        single_parent=True
    )
    cash_transactions = relationship("CashTransaction", back_populates="user", cascade="all, delete-orphan")
    cajas = relationship("Caja", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"
