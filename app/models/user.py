from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class RoleType(str, enum.Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    COLLECTOR = "collector"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(Enum(RoleType))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    assigned_clients = relationship("Client", back_populates="collector")
    supervised_collectors = relationship("User", 
                                      backref="supervisor",
                                      remote_side=[id])
    cash_transactions = relationship("CashTransaction", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
