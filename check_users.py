"""Script para verificar usuarios en la base de datos"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

def main():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\n{'='*60}")
        print(f"Total usuarios en la base de datos: {len(users)}")
        print(f"{'='*60}\n")
        
        if not users:
            print("⚠️ NO HAY USUARIOS EN LA BASE DE DATOS")
            print("\nNecesitas crear un usuario administrador primero.")
            return
        
        for user in users:
            print(f"📋 Usuario:")
            print(f"   ID: {user.id}")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Full Name: {user.full_name}")
            print(f"   Role: {user.role}")
            print(f"   Zone: {user.zone}")
            print(f"   Phone: {user.phone}")
            print(f"   Active: {user.is_active}")
            print(f"   Supervisor ID: {user.supervisor_id}")
            print(f"   Password Hash: {user.hashed_password[:20]}...")
            print()
            
        # Probar autenticación
        print(f"\n{'='*60}")
        print("PRUEBA DE AUTENTICACIÓN")
        print(f"{'='*60}\n")
        test_username = input("Ingresa el username para probar: ").strip()
        test_password = input("Ingresa el password para probar: ").strip()
        
        user = db.query(User).filter(User.username == test_username).first()
        if not user:
            print(f"\n❌ Usuario '{test_username}' NO encontrado en la base de datos")
        else:
            print(f"\n✅ Usuario '{test_username}' encontrado")
            is_valid = verify_password(test_password, user.hashed_password)
            if is_valid:
                print(f"✅ Password CORRECTO - Login debería funcionar")
            else:
                print(f"❌ Password INCORRECTO")
                
    finally:
        db.close()

if __name__ == "__main__":
    main()
