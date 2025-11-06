from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class TransactionType(str, enum.Enum):
    PAYMENT = "payment"          # Pago de cuota
    DISBURSEMENT = "disbursement"  # Desembolso de crédito
    DEPOSIT = "deposit"          # Depósito a caja
    WITHDRAWAL = "withdrawal"    # Retiro de caja

class CashTransaction(Base):
    __tablename__ = "cash_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    credit_id = Column(Integer, ForeignKey("credits.id"), nullable=True)
    amount = Column(Float)
    transaction_type = Column(Enum(TransactionType))
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="cash_transactions")
    credit = relationship("Credit", back_populates="payments")

    def __repr__(self):
        return f"<CashTransaction {self.id} - {self.transaction_type}>"
