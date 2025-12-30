from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Box(Base):
    __tablename__ = "boxes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    base_balance = Column(Float, default=0.0)  # Dinero base (Caja principal)
    insurance_balance = Column(Float, default=0.0)  # Micro seguro (Independiente)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relación con usuario. Usamos backref para no tocar el modelo User existente.
    user = relationship("User", back_populates="box")
    movements = relationship("BoxMovement", back_populates="box")

class BoxMovement(Base):
    __tablename__ = "box_movements"

    id = Column(Integer, primary_key=True, index=True)
    box_id = Column(Integer, ForeignKey("boxes.id"))
    amount = Column(Float, nullable=False)
    movement_type = Column(String, nullable=False)  # TRANSFER_IN, TRANSFER_OUT, EXPENSE, WITHDRAWAL
    description = Column(String, nullable=True)
    is_insurance = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    performed_by_id = Column(Integer, ForeignKey("users.id"))

    box = relationship("Box", back_populates="movements")