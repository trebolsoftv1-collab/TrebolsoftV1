"""
E2E: Valida jerarquía y flujo de créditos con seguro y pagos.

Se ejecuta contra una API en vivo configurando variables de entorno:
- BASE_URL (ej: https://trebolsoft.com)
- ADMIN_USERNAME (ej: admin)
- ADMIN_PASSWORD (ej: Admin123!)

El test crea recursos con sufijos aleatorios para evitar colisiones.
"""
import os
import time
import random
import string
import requests
import pytest


def _rand(n: int = 6) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def _require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        pytest.skip(f"Falta variable de entorno: {name}")
    return val


def login(base_url: str, username: str, password: str) -> str:
    r = requests.post(
        f"{base_url}/api/v1/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    assert r.status_code == 200, f"login fallo: {r.status_code} {r.text}"
    return r.json()["access_token"]


def create_user(base_url: str, token: str, payload: dict) -> dict:
    r = requests.post(
        f"{base_url}/api/v1/users",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    assert r.status_code == 201, f"crear usuario fallo: {r.status_code} {r.text}"
    return r.json()


def create_client(base_url: str, token: str, payload: dict) -> dict:
    r = requests.post(
        f"{base_url}/api/v1/clients",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    assert r.status_code == 201, f"crear cliente fallo: {r.status_code} {r.text}"
    return r.json()


def create_credit(base_url: str, token: str, payload: dict) -> dict:
    r = requests.post(
        f"{base_url}/api/v1/credits",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    assert r.status_code == 201, f"crear credito fallo: {r.status_code} {r.text}"
    return r.json()


def get_credit(base_url: str, token: str, credit_id: int) -> dict:
    r = requests.get(
        f"{base_url}/api/v1/credits/{credit_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    assert r.status_code == 200, f"obtener credito fallo: {r.status_code} {r.text}"
    return r.json()


def create_payment(base_url: str, token: str, credit_id: int, amount: float) -> dict:
    r = requests.post(
        f"{base_url}/api/v1/transactions",
        json={
            "transaction_type": "payment",
            "credit_id": credit_id,
            "amount": amount,
        },
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    assert r.status_code == 201, f"crear pago fallo: {r.status_code} {r.text}"
    return r.json()


@pytest.mark.e2e
def test_credit_with_insurance_and_payments():
    base_url = _require_env("BASE_URL")
    admin_user = _require_env("ADMIN_USERNAME")
    admin_pass = _require_env("ADMIN_PASSWORD")

    admin_token = login(base_url, admin_user, admin_pass)

    suf = _rand()

    # 1) Admin crea supervisor
    supervisor = create_user(
        base_url,
        admin_token,
        {
            "username": f"sup_{suf}",
            "full_name": f"Supervisor {suf}",
            "role": "supervisor",
            "password": "Sup123!a",
            "supervisor_id": None,
        },
    )
    sup_token = login(base_url, supervisor["username"], "Sup123!a")

    # 2) Supervisor crea cobrador
    collector = create_user(
        base_url,
        sup_token,
        {
            "username": f"col_{suf}",
            "full_name": f"Collector {suf}",
            "role": "collector",
            "password": "Col123!a",
        },
    )
    col_id = collector["id"]

    # 3) Supervisor crea cliente para ese cobrador
    client = create_client(
        base_url,
        sup_token,
        {
            "dni": f"99{suf}01",
            "full_name": f"Cliente {suf}",
            "address": "Calle 123",
            "phone": "999000111",
            "collector_id": col_id,
        },
    )

    # 4) Supervisor crea crédito con seguro
    amount = 1000.0
    interest = 10.0
    insurance = 50.0
    term_days = 50

    credit = create_credit(
        base_url,
        sup_token,
        {
            "client_id": client["id"],
            "amount": amount,
            "interest_rate": interest,
            "term_days": term_days,
            "insurance_amount": insurance,
        },
    )

    # total esperado: 1000 * 1.10 + 50 = 1150; daily = 23
    assert abs(credit["total_amount"] - 1150.0) < 1e-6
    assert abs(credit["daily_payment"] - 23.0) < 1e-6
    assert abs(credit["remaining_amount"] - 1150.0) < 1e-6

    # 5) Cobrador paga 100 y se reduce el saldo
    col_token = login(base_url, collector["username"], "Col123!a")
    tx = create_payment(base_url, col_token, credit["id"], 100.0)

    # refrescar crédito
    credit2 = get_credit(base_url, sup_token, credit["id"])  # supervisor puede ver
    assert abs(credit2["remaining_amount"] - 1050.0) < 1e-6
    assert credit2["status"] == "active"

    # 6) Pagos hasta completar
    # (para no golpear demasiado el endpoint, hacemos dos pagos grandes)
    tx2 = create_payment(base_url, col_token, credit["id"], 1000.0)
    credit3 = get_credit(base_url, sup_token, credit["id"])  # 50 restantes
    assert abs(credit3["remaining_amount"] - 50.0) < 1e-6

    tx3 = create_payment(base_url, col_token, credit["id"], 50.0)
    credit4 = get_credit(base_url, sup_token, credit["id"])  # 0 restantes
    assert abs(credit4["remaining_amount"] - 0.0) < 1e-6
    assert credit4["status"] == "completed"
