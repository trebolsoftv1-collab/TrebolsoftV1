# sync-forced-2025
"""
Script para resetear la contraseña de un usuario existente
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def reset_password():
    """Resetea la contraseña de un usuario"""
    db = SessionLocal()
    try:
        # Listar usuarios
        users = db.query(User).all()
        if not users:
            print("❌ No hay usuarios en la base de datos")
            print("💡 Ejecuta create_admin.py primero")
            return
        
        print("\n" + "="*60)
        print("USUARIOS DISPONIBLES")
        print("="*60)
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.username} ({user.email}) - Role: {user.role}")
        
        # Seleccionar usuario
        print("\n" + "="*60)
        selection = input("Ingresa el número del usuario a resetear: ").strip()
        try:
            idx = int(selection) - 1
            if idx < 0 or idx >= len(users):
                print("❌ Selección inválida")
                return
            user = users[idx]
        except ValueError:
            print("❌ Debes ingresar un número")
            return
        
        # Nueva contraseña
        new_password = input(f"\nIngresa la nueva contraseña para '{user.username}': ").strip()
        if len(new_password) < 6:
            print("❌ La contraseña debe tener al menos 6 caracteres")
            return
        
        # Confirmar
        confirm = input(f"\n⚠️  ¿Confirmas resetear la contraseña de '{user.username}'? (si/no): ").strip().lower()
        if confirm not in ['si', 's', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
        
        # Actualizar contraseña
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        
        print("\n" + "="*60)
        print("✅ CONTRASEÑA ACTUALIZADA EXITOSAMENTE")
        print("="*60)
        print(f"\n📋 Credenciales actualizadas:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Nueva Password: {new_password}")
        print(f"\n🌐 Ahora puedes iniciar sesión en:")
        print(f"   - https://app.trebolsoft.com")
        print(f"   - http://localhost:8000/docs")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error reseteando contraseña: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_password()
