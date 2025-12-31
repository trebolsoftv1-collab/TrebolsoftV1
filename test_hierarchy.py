# sync-forced-2025
"""Script para probar la jerarquía de usuarios y permisos."""
import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def login(username: str, password: str):
    """Obtiene token JWT."""
    response = requests.post(
        f"{BASE_URL}/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login exitoso: {username}")
        return token
    else:
        print(f"❌ Error login {username}: {response.status_code} - {response.text}")
        return None

def create_user(token: str, user_data: dict):
    """Crea un usuario."""
    response = requests.post(
        f"{BASE_URL}/users",
        json=user_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 201:
        user = response.json()
        print(f"✅ Usuario creado: {user['username']} (ID: {user['id']}, role: {user['role']})")
        return user
    else:
        print(f"❌ Error creando usuario: {response.status_code} - {response.text}")
        return None

def list_users(token: str, username: str):
    """Lista usuarios visibles."""
    response = requests.get(
        f"{BASE_URL}/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        users = response.json()
        print(f"✅ Usuarios visibles para {username}: {len(users)}")
        for u in users:
            print(f"   - {u['username']} (role: {u['role']}, supervisor_id: {u.get('supervisor_id')})")
        return users
    else:
        print(f"❌ Error listando usuarios: {response.status_code}")
        return []

def create_client(token: str, client_data: dict):
    """Crea un cliente."""
    response = requests.post(
        f"{BASE_URL}/clients",
        json=client_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 201:
        client = response.json()
        print(f"✅ Cliente creado: {client['full_name']} (ID: {client['id']}, collector_id: {client['collector_id']})")
        return client
    else:
        print(f"❌ Error creando cliente: {response.status_code} - {response.text}")
        return None

def list_clients(token: str, username: str):
    """Lista clientes visibles."""
    response = requests.get(
        f"{BASE_URL}/clients",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        clients = response.json()
        print(f"✅ Clientes visibles para {username}: {len(clients)}")
        for c in clients:
            print(f"   - {c['full_name']} (DNI: {c['dni']}, collector_id: {c['collector_id']})")
        return clients
    else:
        print(f"❌ Error listando clientes: {response.status_code}")
        return []

def main():
    print("=" * 60)
    print("🧪 TEST DE JERARQUÍA: Admin → Supervisor → Cobrador")
    print("=" * 60)
    
    # 1. Login como Admin
    print("\n📋 PASO 1: Login Admin")
    admin_token = login("admin", "Admin123!")
    if not admin_token:
        return
    
    # 2. Admin lista usuarios (debe ver solo a sí mismo por ahora)
    print("\n📋 PASO 2: Admin lista usuarios")
    list_users(admin_token, "admin")
    
    # 3. Admin crea Supervisor
    print("\n📋 PASO 3: Admin crea Supervisor")
    supervisor = create_user(admin_token, {
        "email": "supervisor1@trebolsoft.com",
        "username": "supervisor1",
        "full_name": "Juan Supervisor",
        "role": "supervisor",
        "password": "Super123!",
        "supervisor_id": None
    })
    if not supervisor:
        return
    
    # 4. Login como Supervisor
    print("\n📋 PASO 4: Login Supervisor")
    supervisor_token = login("supervisor1", "Super123!")
    if not supervisor_token:
        return
    
    # 5. Supervisor crea Cobrador 1
    print("\n📋 PASO 5: Supervisor crea Cobrador 1")
    collector1 = create_user(supervisor_token, {
        "email": "cobrador1@trebolsoft.com",
        "username": "cobrador1",
        "full_name": "Carlos Cobrador Uno",
        "role": "collector",
        "password": "Cobra123!"
    })
    if not collector1:
        return
    
    # 6. Supervisor crea Cobrador 2
    print("\n📋 PASO 6: Supervisor crea Cobrador 2")
    collector2 = create_user(supervisor_token, {
        "email": "cobrador2@trebolsoft.com",
        "username": "cobrador2",
        "full_name": "Pedro Cobrador Dos",
        "role": "collector",
        "password": "Cobra456!"
    })
    if not collector2:
        return
    
    # 7. Login como Cobrador 1
    print("\n📋 PASO 7: Login Cobrador 1")
    collector1_token = login("cobrador1", "Cobra123!")
    if not collector1_token:
        return
    
    # 8. Cobrador 1 crea Cliente 1
    print("\n📋 PASO 8: Cobrador 1 crea Cliente (como supervisor)")
    print("⚠️  Nota: Solo supervisores pueden crear clientes, cobrador1 debería fallar")
    client1 = create_client(collector1_token, {
        "dni": "12345678",
        "full_name": "Cliente Uno",
        "address": "Calle 123",
        "phone": "999111222",
        "collector_id": collector1["id"]
    })
    
    # 9. Supervisor crea clientes para sus cobradores
    print("\n📋 PASO 9: Supervisor crea clientes para cobradores")
    client_c1 = create_client(supervisor_token, {
        "dni": "11111111",
        "full_name": "Cliente de Cobrador 1",
        "address": "Av. Principal 100",
        "phone": "999111111",
        "collector_id": collector1["id"]
    })
    
    client_c2 = create_client(supervisor_token, {
        "dni": "22222222",
        "full_name": "Cliente de Cobrador 2",
        "address": "Av. Secundaria 200",
        "phone": "999222222",
        "collector_id": collector2["id"]
    })
    
    # Supervisor crea cliente propio
    client_supervisor = create_client(supervisor_token, {
        "dni": "99999999",
        "full_name": "Cliente Propio del Supervisor",
        "address": "Av. Jefe 999",
        "phone": "999999999",
        "collector_id": supervisor["id"]
    })
    
    # 10. Prueba de visibilidad
    print("\n📋 PASO 10: Pruebas de visibilidad")
    print("\n👁️  Admin ve todos los usuarios:")
    list_users(admin_token, "admin")
    
    print("\n👁️  Supervisor ve sus cobradores:")
    list_users(supervisor_token, "supervisor1")
    
    print("\n👁️  Cobrador 1 ve solo a sí mismo:")
    list_users(collector1_token, "cobrador1")
    
    print("\n👁️  Admin ve todos los clientes:")
    list_clients(admin_token, "admin")
    
    print("\n👁️  Supervisor ve clientes de sus cobradores + propios:")
    list_clients(supervisor_token, "supervisor1")
    
    print("\n👁️  Cobrador 1 ve solo sus clientes:")
    list_clients(collector1_token, "cobrador1")
    
    # 11. Verificación de Reglas de Asignación
    print("\n📋 PASO 11: Verificación de Reglas de Asignación (Lógica esperada)")
    print("-" * 50)
    print("   👉 COBRADOR: Al crear, el backend debe ignorar 'collector_id' enviado y forzar el ID del usuario actual.")
    print("      Resultado: Cliente asignado a Cobrador 1 automáticamente.")
    
    print("\n   👉 SUPERVISOR: Debe enviar 'collector_id'. El backend debe validar que ese cobrador sea su subordinado.")
    print("      UI: Debe mostrar dropdown solo con sus cobradores.")
    
    print("\n   👉 ADMIN: Debe enviar 'collector_id'. Puede elegir cualquier cobrador del sistema.")
    print("      UI: Debe mostrar selector de Supervisor (filtro) y luego selector de Cobrador.")
    print("-" * 50)

    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
