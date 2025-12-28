import sys
import os

# Aseguramos que el directorio raiz del proyecto este en el path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        # 1. Buscar si el usuario ya existe
        user = db.query(User).filter(User.username == "trebolsoft").first()
        
        if user:
            print(f"🔄 El usuario 'trebolsoft' ya existe. Actualizando permisos...")
            user.is_superuser = True
            user.is_active = True
            # Aseguramos que la contraseña sea la correcta si es necesario, o la dejamos
            # user.hashed_password = get_password_hash("Admin123!") 
        else:
            print(f"🆕 Creando usuario 'trebolsoft' nuevo...")
            user = User(
                username="trebolsoft",
                email="admin@trebolsoft.com",
                hashed_password=get_password_hash("Admin123!"),
                is_active=True,
                is_superuser=True
            )
            db.add(user)
        
        db.commit()
        print("✅ ¡ÉXITO! Usuario administrador configurado correctamente en DigitalOcean.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
