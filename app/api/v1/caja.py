from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.caja import Caja, CajaTipo, CajaMovimiento, MovimientoTipo, TopePrestamo
from app.models.user import User, RoleType
from app.models.client import Client
from app.crud.caja import *

router = APIRouter()

@router.post("/caja/create/{user_id}")
def create_cajas(user_id: int, db: Session = Depends(get_db)):
    create_cajas_for_user(db, user_id)
    return {"msg": "Cajas creadas"}

@router.post("/caja/transferir")
def transferir_base_api(supervisor_id: int, cobrador_id: int, monto: float, db: Session = Depends(get_db)):
    ok = transferir_base(db, supervisor_id, cobrador_id, monto)
    if not ok:
        raise HTTPException(status_code=400, detail="Saldo insuficiente o cajas no encontradas")
    return {"msg": "Transferencia realizada"}

@router.post("/caja/gasto")
def registrar_gasto_api(caja_id: int, monto: float, descripcion: str, usuario_id: int, db: Session = Depends(get_db)):
    ok = registrar_gasto(db, caja_id, monto, descripcion, usuario_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Saldo insuficiente o caja no encontrada")
    return {"msg": "Gasto registrado"}

@router.post("/caja/microseguro")
def registrar_microseguro_api(caja_id: int, monto: float, cliente_id: int, usuario_id: int, db: Session = Depends(get_db)):
    ok = registrar_microseguro(db, caja_id, monto, cliente_id, usuario_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Caja microseguro no encontrada")
    return {"msg": "Microseguro registrado"}

@router.post("/caja/retiro")
def registrar_retiro_api(caja_id: int, monto: float, usuario_id: int, destino_supervisor: bool = False, db: Session = Depends(get_db)):
    ok = registrar_retiro(db, caja_id, monto, usuario_id, destino_supervisor)
    if not ok:
        raise HTTPException(status_code=400, detail="Saldo insuficiente o caja no encontrada")
    return {"msg": "Retiro registrado"}

@router.post("/caja/cierre")
def registrar_cierre_caja_api(caja_id: int, usuario_id: int, saldo_final: float, observaciones: str = None, db: Session = Depends(get_db)):
    registrar_cierre_caja(db, caja_id, usuario_id, saldo_final, observaciones)
    return {"msg": "Cierre de caja registrado"}

@router.post("/caja/volado")
def marcar_cliente_volado_api(cliente_id: int, monto_bloqueado: float, usuario_id: int, observaciones: str = None, db: Session = Depends(get_db)):
    ok = marcar_cliente_volado(db, cliente_id, monto_bloqueado, usuario_id, observaciones)
    if not ok:
        raise HTTPException(status_code=400, detail="Cliente no encontrado")
    return {"msg": "Cliente marcado como volado"}

@router.post("/caja/tope")
def actualizar_tope_prestamo_api(supervisor_id: int, cobrador_id: int, monto_maximo: float, db: Session = Depends(get_db)):
    tope = actualizar_tope_prestamo(db, supervisor_id, cobrador_id, monto_maximo)
    return {"msg": "Tope actualizado", "tope": tope.monto_maximo}

# Aquí se pueden agregar endpoints GET para consultar movimientos, saldos, cierres, volados, etc.
