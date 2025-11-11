"""
Script para resetear la contraseña del admin conectándose directamente a la base de datos
"""
import psycopg2
from passlib.context import CryptContext

# Configuración de bcrypt (mismo que usa FastAPI)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Conexión a la base de datos
DATABASE_URL = "postgresql://trebolsoft_db_user:FtxaQLZgsVV6LIFMACP6cA07xea67d1Va@dpg-d3tokphDhihsf3aibh70-a.oregon-postgres.render.com:5432/trebolsoft_db"

try:
    # Conectar
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    # Ver usuarios admin actuales
    cursor.execute("SELECT id, username, email, role, is_active FROM users WHERE role='admin';")
    admins = cursor.fetchall()
    
    print("=== USUARIOS ADMIN ACTUALES ===")
    for admin in admins:
        print(f"ID: {admin[0]}, Username: {admin[1]}, Email: {admin[2]}, Role: {admin[3]}, Active: {admin[4]}")
    
    if admins:
        # Resetear contraseña del primer admin
        new_password = "Admin123!"
        hashed = pwd_context.hash(new_password)
        
        cursor.execute(
            "UPDATE users SET hashed_password = %s WHERE username = 'admin';",
            (hashed,)
        )
        conn.commit()
        print(f"\n✅ Contraseña del admin actualizada a: {new_password}")
    else:
        print("\n❌ No se encontró ningún usuario admin")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
