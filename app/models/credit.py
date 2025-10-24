from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    installments = Column(Integer, nullable=False, default=1)
    insurance_amount = Column(Numeric(12,2), nullable=True, default=0)
    balance = Column(Numeric(12,2), nullable=False)
    status = Column(String, nullable=False, default="active")
    start_date = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client", backref="credits")
