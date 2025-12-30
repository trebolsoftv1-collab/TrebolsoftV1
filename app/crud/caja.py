from sqlalchemy.orm import Session
from app.models.caja import Caja, CajaMovimiento, CajaTipo, MovimientoTipo, TopePrestamo
from app.models.user import User
from app.models.credit import Credit
from app.models.client import Client
from datetime import datetime

# Crear caja principal y microseguro para usuario

def create_cajas_for_user(db: Session, user_id: int):
    for tipo in [CajaTipo.PRINCIPAL, CajaTipo.MICROSEGURO]:
        caja = Caja(user_id=user_id, tipo=tipo, saldo=0.0)
        db.add(caja)
    db.commit()

# Registrar movimiento en caja

def registrar_movimiento(db: Session, caja_id: int, tipo: MovimientoTipo, monto: float, descripcion: str = None, usuario_origen_id: int = None, usuario_destino_id: int = None, credito_id: int = None, cliente_id: int = None, observaciones: str = None):
    movimiento = CajaMovimiento(
        caja_id=caja_id,
        tipo=tipo,
        monto=monto,
        descripcion=descripcion,
        usuario_origen_id=usuario_origen_id,
        usuario_destino_id=usuario_destino_id,
        credito_id=credito_id,
        cliente_id=cliente_id,
        observaciones=observaciones,
        created_at=datetime.utcnow()
    )
    db.add(movimiento)
    db.commit()
    return movimiento

# Transferir base de supervisor a cobrador

def transferir_base(db: Session, supervisor_id: int, cobrador_id: int, monto: float):
    supervisor_caja = db.query(Caja).filter_by(user_id=supervisor_id, tipo=CajaTipo.PRINCIPAL).first()
    cobrador_caja = db.query(Caja).filter_by(user_id=cobrador_id, tipo=CajaTipo.PRINCIPAL).first()
    if supervisor_caja and cobrador_caja and supervisor_caja.saldo >= monto:
        supervisor_caja.saldo -= monto
        cobrador_caja.saldo += monto
        db.commit()
        registrar_movimiento(db, supervisor_caja.id, MovimientoTipo.TRANSFERENCIA, -monto, f"Transferencia a cobrador {cobrador_id}", usuario_origen_id=supervisor_id, usuario_destino_id=cobrador_id)
        registrar_movimiento(db, cobrador_caja.id, MovimientoTipo.INGRESO, monto, f"Recibido de supervisor {supervisor_id}", usuario_origen_id=supervisor_id, usuario_destino_id=cobrador_id)
        return True
    return False

# Registrar gasto

def registrar_gasto(db: Session, caja_id: int, monto: float, descripcion: str, usuario_id: int):
    caja = db.query(Caja).filter_by(id=caja_id).first()
    if caja and caja.saldo >= monto:
        caja.saldo -= monto
        db.commit()
        registrar_movimiento(db, caja.id, MovimientoTipo.GASTO, -monto, descripcion, usuario_origen_id=usuario_id)
        return True
    return False

# Registrar microseguro

def registrar_microseguro(db: Session, caja_id: int, monto: float, cliente_id: int, usuario_id: int):
    caja = db.query(Caja).filter_by(id=caja_id, tipo=CajaTipo.MICROSEGURO).first()
    if caja:
        caja.saldo += monto
        db.commit()
        registrar_movimiento(db, caja.id, MovimientoTipo.MICROSEGURO, monto, "Microseguro cobrado", usuario_origen_id=usuario_id, cliente_id=cliente_id)
        return True
    return False

# Registrar retiro

def registrar_retiro(db: Session, caja_id: int, monto: float, usuario_id: int, destino_supervisor: bool = False):
    caja = db.query(Caja).filter_by(id=caja_id).first()
    if caja and caja.saldo >= monto:
        caja.saldo -= monto
        db.commit()
        registrar_movimiento(db, caja.id, MovimientoTipo.RETIRO, -monto, "Retiro de caja", usuario_origen_id=usuario_id)
        if destino_supervisor:
            # El dinero pasa a la caja del supervisor
            supervisor_caja = db.query(Caja).filter_by(user_id=usuario_id, tipo=CajaTipo.PRINCIPAL).first()
            if supervisor_caja:
                supervisor_caja.saldo += monto
                db.commit()
                registrar_movimiento(db, supervisor_caja.id, MovimientoTipo.INGRESO, monto, "Recibido por retiro de cobrador", usuario_origen_id=usuario_id)
        return True
    return False

# Registrar cierre de caja

def registrar_cierre_caja(db: Session, caja_id: int, usuario_id: int, saldo_final: float, observaciones: str = None):
    registrar_movimiento(db, caja_id, MovimientoTipo.CIERRE, saldo_final, "Cierre de caja", usuario_origen_id=usuario_id, observaciones=observaciones)

# Marcar cliente como volado

def marcar_cliente_volado(db: Session, cliente_id: int, monto_bloqueado: float, usuario_id: int, observaciones: str = None):
    cliente = db.query(Client).filter_by(id=cliente_id).first()
    if cliente:
        cliente.estado = "volado"
        db.commit()
        registrar_movimiento(db, None, MovimientoTipo.VOLADO, monto_bloqueado, "Cliente volado", usuario_origen_id=usuario_id, cliente_id=cliente_id, observaciones=observaciones)
        return True
    return False

# Actualizar tope de préstamo

def actualizar_tope_prestamo(db: Session, supervisor_id: int, cobrador_id: int, monto_maximo: float):
    tope = db.query(TopePrestamo).filter_by(supervisor_id=supervisor_id, cobrador_id=cobrador_id).first()
    if not tope:
        tope = TopePrestamo(supervisor_id=supervisor_id, cobrador_id=cobrador_id, monto_maximo=monto_maximo)
        db.add(tope)
    else:
        tope.monto_maximo = monto_maximo
    db.commit()
    return tope
