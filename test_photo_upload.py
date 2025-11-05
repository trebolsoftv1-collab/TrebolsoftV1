"""
Script de prueba para verificar el endpoint de upload de fotos.
Ejecutar después de que el deploy esté completo en Render.
"""

import requests
import os

# Configuración
API_URL = "https://trebolsoft.onrender.com"  # Cambia si usas otra URL
USERNAME = "admin"  # Cambia por tu usuario admin
PASSWORD = "tu_password"  # Cambia por tu contraseña

def test_photo_upload():
    """Prueba el flujo completo de subida de foto."""
    
    print("🔐 1. Haciendo login...")
    # Login
    login_response = requests.post(
        f"{API_URL}/api/v1/auth/token",
        data={"username": USERNAME, "password": PASSWORD}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Error en login: {login_response.status_code}")
        print(login_response.json())
        return
    
    token = login_response.json()["access_token"]
    print(f"✅ Login exitoso. Token: {token[:20]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n👥 2. Creando cliente de prueba...")
    # Crear cliente
    client_data = {
        "dni": "TEST12345",
        "full_name": "Cliente Prueba Foto",
        "address": "Calle Test 123",
        "phone": "555-1234",
        "latitude": 4.7110,
        "longitude": -74.0721
    }
    
    client_response = requests.post(
        f"{API_URL}/api/v1/clients/",
        json=client_data,
        headers=headers
    )
    
    if client_response.status_code not in [200, 201]:
        print(f"❌ Error creando cliente: {client_response.status_code}")
        print(client_response.json())
        return
    
    client = client_response.json()
    client_id = client["id"]
    print(f"✅ Cliente creado con ID: {client_id}")
    print(f"   Ubicación: {client.get('latitude')}, {client.get('longitude')}")
    print(f"   Google Maps: {client.get('google_maps_url')}")
    
    print(f"\n📸 3. Verificando endpoint de upload...")
    # Verificar que el endpoint existe
    docs_response = requests.get(f"{API_URL}/docs")
    if docs_response.status_code == 200:
        print("✅ API docs accesible")
    
    # Crear una imagen de prueba (1x1 pixel PNG)
    test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    print(f"\n📤 4. Subiendo foto al cliente {client_id}...")
    files = {"file": ("test.png", test_image, "image/png")}
    
    upload_response = requests.post(
        f"{API_URL}/api/v1/clients/{client_id}/upload-photo",
        files=files,
        headers=headers
    )
    
    if upload_response.status_code == 200:
        result = upload_response.json()
        print("✅ Foto subida exitosamente!")
        print(f"   URL: {result.get('photo_url')}")
        print(f"   Mensaje: {result.get('message')}")
    else:
        print(f"❌ Error subiendo foto: {upload_response.status_code}")
        print(upload_response.json())
        return
    
    print(f"\n🔍 5. Verificando cliente actualizado...")
    # Verificar cliente
    verify_response = requests.get(
        f"{API_URL}/api/v1/clients/{client_id}",
        headers=headers
    )
    
    if verify_response.status_code == 200:
        updated_client = verify_response.json()
        print("✅ Cliente actualizado:")
        print(f"   house_photo_url: {updated_client.get('house_photo_url')}")
        print(f"   google_maps_url: {updated_client.get('google_maps_url')}")
    
    print("\n🎉 ¡Prueba completada exitosamente!")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Test de subida de fotos a TrebolSoft API")
    print("=" * 60)
    print()
    test_photo_upload()
