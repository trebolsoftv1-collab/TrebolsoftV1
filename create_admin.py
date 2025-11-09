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
        existing_admin = db.query(User).filter(User.role == RoleType.ADMIN).first()
        if existing_admin:
            print(f"✅ Ya existe un administrador: {existing_admin.username}")
            print(f"   Email: {existing_admin.email}")
            print(f"\n💡 Si olvidaste la contraseña, usa reset_password.py")
            return
        
        # Datos del admin por defecto
        admin_data = {
            "username": "admin",
            "email": "admin@trebolsoft.com",
            "full_name": "Administrador",
            "phone": "0000000000",
            "zone": "Todas",
            "role": RoleType.ADMIN,
            "is_active": True,
            "hashed_password": get_password_hash("admin123"),  # Cambiar después del primer login
            "supervisor_id": None
        }
        
        # Crear usuario
        admin_user = User(**admin_data)
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("="*60)
        print("✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
        print("="*60)
        print(f"\n📋 Credenciales de acceso:")
        print(f"   Username: {admin_user.username}")
        print(f"   Password: admin123")
        print(f"   Email: {admin_user.email}")
        print(f"   Role: {admin_user.role}")
        print(f"\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
        print(f"\n🌐 Puedes usar estas credenciales en:")
        print(f"   - https://app.trebolsoft.com")
        print(f"   - http://localhost:8000/docs")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error creando administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
