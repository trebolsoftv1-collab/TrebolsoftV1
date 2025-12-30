from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class CajaTipo(str, enum.Enum):
    PRINCIPAL = "principal"
    MICROSEGURO = "microseguro"

class Caja(Base):
    __tablename__ = "cajas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    tipo = Column(Enum(CajaTipo), default=CajaTipo.PRINCIPAL)
    saldo = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="cajas")
    movimientos = relationship("CajaMovimiento", back_populates="caja")

class MovimientoTipo(str, enum.Enum):
    INGRESO = "ingreso"
    EGRESO = "egreso"
    TRANSFERENCIA = "transferencia"
    RETIRO = "retiro"
    GASTO = "gasto"
    MICROSEGURO = "microseguro"
    PRESTAMO = "prestamo"
    ABONO = "abono"
    VOLADO = "volado"
    CIERRE = "cierre"

class CajaMovimiento(Base):
    __tablename__ = "caja_movimientos"

    id = Column(Integer, primary_key=True, index=True)
    caja_id = Column(Integer, ForeignKey("cajas.id"), index=True)
    tipo = Column(Enum(MovimientoTipo))
    monto = Column(Float)
    descripcion = Column(String, nullable=True)
    usuario_origen_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    usuario_destino_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    credito_id = Column(Integer, ForeignKey("credits.id"), nullable=True)
    cliente_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    observaciones = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    caja = relationship("Caja", back_populates="movimientos")
    usuario_origen = relationship("User", foreign_keys=[usuario_origen_id])
    usuario_destino = relationship("User", foreign_keys=[usuario_destino_id])
    credito = relationship("Credit")
    cliente = relationship("Client")

class TopePrestamo(Base):
    __tablename__ = "topes_prestamo"

    id = Column(Integer, primary_key=True, index=True)
    supervisor_id = Column(Integer, ForeignKey("users.id"), index=True)
    cobrador_id = Column(Integer, ForeignKey("users.id"), index=True)
    monto_maximo = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    supervisor = relationship("User", foreign_keys=[supervisor_id])
    cobrador = relationship("User", foreign_keys=[cobrador_id])

class EstadoCliente(str, enum.Enum):
    ACTIVO = "activo"
    VOLADO = "volado"
    RECUPERADO = "recuperado"

# NOTA: El campo estado se debe agregar al modelo Client existente
