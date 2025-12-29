from sqlalchemy import func
from app.models.cash_transaction import CashTransaction
from app.models.client import Client
from app.models.credit import Credit, CreditStatus

def get_stats(db, start_date=None, end_date=None, user_ids=None):
    # Consultas base
    tx_query = db.query(CashTransaction)
    client_query = db.query(Client)
    credit_query = db.query(Credit)
    
    # 1. Filtrar por usuarios (si se especifica lista)
    if user_ids is not None:
        tx_query = tx_query.filter(CashTransaction.user_id.in_(user_ids))
        client_query = client_query.filter(Client.collector_id.in_(user_ids))
        # Para créditos, filtramos por el cobrador del cliente asociado
        credit_query = credit_query.join(Client).filter(Client.collector_id.in_(user_ids))

    # 2. Filtrar por fechas (Aplica principalmente a transacciones/cobros)
    if start_date:
        tx_query = tx_query.filter(func.date(CashTransaction.created_at) >= start_date)
    if end_date:
        tx_query = tx_query.filter(func.date(CashTransaction.created_at) <= end_date)

    # 3. Calcular totales
    # Total cobrado (suma de montos)
    total_cobrado = tx_query.with_entities(func.sum(CashTransaction.amount)).scalar() or 0
    
    # Cantidad de cobros realizados
    total_transacciones = tx_query.count()
    
    # Totales de clientes y créditos (estos suelen ser totales históricos, no por rango de fecha, salvo creación)
    # Solo contamos clientes ACTIVOS para que el número sea real
    total_clientes = client_query.filter(Client.is_active == True).count()
    active_credits = credit_query.filter(Credit.status == CreditStatus.ACTIVE).count()
    completed_credits = credit_query.filter(Credit.status == CreditStatus.COMPLETED).count()

    return {
        "total_cobranzas": total_transacciones,
        "total_clientes": total_clientes,
        "total_pendientes": active_credits,
        "total_realizadas": completed_credits,
        "monto_total": total_cobrado,
    }
