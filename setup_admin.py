# sync-forced-2025
"""
Script de setup inicial - Ejecutar manualmente para crear admin
"""
import requests

API_URL = "https://api.trebolsoft.com"

# Endpoint temporal de setup (crear en main.py)
response = requests.post(f"{API_URL}/setup-admin", json={
    "username": "admin",
    "password": "Admin123!",
    "email": "admin@trebolsoft.com",
    "full_name": "Administrador"
})

if response.status_code == 200:
    print("✅ Admin creado exitosamente")
    print(response.json())
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
