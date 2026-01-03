from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class CreditStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    defaulted = "defaulted"

class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float)
    interest_rate = Column(Float)  # Tasa de interés en porcentaje
    term_days = Column(Integer)    # Plazo en días
    insurance_amount = Column(Float, default=0.0)  # Seguro asociado al crédito
    daily_payment = Column(Float)  # Pago diario calculado
    total_amount = Column(Float)   # Monto total a pagar
    remaining_amount = Column(Float) # Monto restante por pagar
    status = Column(Enum(CreditStatus), default=CreditStatus.active)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

        # Cambio automático forzado por sincronización (Copilot 2025-12-31)
    # Cambio automático forzado por sincronización (Copilot 2025-12-31)
    # Relaciones
    client = relationship("Client", back_populates="credits")
    payments = relationship("CashTransaction", back_populates="credit")

    def __repr__(self):
        return f"<Credit {self.id} - Client {self.client_id}>"
