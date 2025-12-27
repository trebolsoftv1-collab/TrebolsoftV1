"""
Script para crear usuario administrador inicial en TrebolSoft
Usar este script cuando no puedes hacer login porque no hay usuarios.
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.user import User, RoleType
from app.core.security import get_password_hash

def create_admin():
    """Crea un usuario administrador por defecto"""
    db = SessionLocal()
    try:
        # Verificar si ya existe un admin
        existing_admin = db.query(User).filter(User.role == 'ADMIN').first()
        if existing_admin:
            print(f"✅ Ya existe un administrador: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"\n💡 Si olvidaste la contraseña, usa reset_password.py")
            return

        # Pedir datos al usuario
        print("\n=== Crear usuario administrador o personalizado ===")
        username = input("Nombre de usuario: ").strip()
        email = input("Email: ").strip()
        full_name = input("Nombre completo: ").strip()
        phone = input("Teléfono: ").strip()
        zone = input("Zona: ").strip()
        password = input("Contraseña: ").strip()
        role = input("Rol (ADMIN/SUPERVISOR/COLLECTOR): ").strip().upper()
        if role not in ["ADMIN", "SUPERVISOR", "COLLECTOR"]:
            print("❌ Rol inválido. Debe ser ADMIN, SUPERVISOR o COLLECTOR.")
            db.close()
            return

        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "phone": phone,
            "zone": zone,
            "role": role,
            "is_active": True,
            "hashed_password": get_password_hash(password),
            "supervisor_id": None
        }

        # Crear usuario
        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("="*60)
        print("✅ USUARIO CREADO EXITOSAMENTE")
        print("="*60)
        print(f"\n📋 Credenciales de acceso:")
        print(f"   Username: {new_user.username}")
        print(f"   Password: {password}")
        print(f"   Email: {new_user.email}")
        print(f"   Role: {new_user.role}")
        print(f"\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        print(f"\n🌐 Puedes usar estas credenciales en:")
        print(f"   - https://www.trebolsoft.com")
        print(f"   - https://trebolsoft.com")
        print(f"   - http://localhost:8000/docs")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error creando administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
