# Ejecuta el test E2E contra una API en vivo.
# Requisitos: pytest y requests instalados en el venv.

param(
    [string]$BaseUrl = "https://trebolsoft.com",
    [string]$AdminUser = "admin",
    [string]$AdminPass = "Admin123!"
)

$env:BASE_URL = $BaseUrl
$env:ADMIN_USERNAME = $AdminUser
$env:ADMIN_PASSWORD = $AdminPass

Write-Host "Running E2E tests against $BaseUrl ..."

# Activar venv si procede
if (Test-Path .\.venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
}

# Instalar pytest si falta
try {
    python -c "import pytest" | Out-Null
} catch {
    pip install pytest | Out-Null
}

pytest -q tests/e2e/test_credit_insurance_flow.py -k e2e