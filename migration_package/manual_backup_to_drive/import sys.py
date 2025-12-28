import sys
import os

# --- CORRECCIÓN DE RUTA ---
# 1. Obtenemos la ruta absoluta de este script (scripts/create_superuser_prod.py)
current_script_path = os.path.abspath(__file__)
# 2. Obtenemos el directorio del script (scripts/)
script_dir = os.path.dirname(current_script_path)
# 3. Obtenemos la raíz del proyecto (TrebolsoftV1/) subiendo un nivel
project_root = os.path.dirname(script_dir)

# 4. ¡IMPORTANTE! Insertamos la raíz al PRINCIPIO de sys.path
# Esto obliga a Python a buscar 'app' en tu carpeta de proyecto primero
sys.path.insert(0, project_root)

print(f"📂 Directorio del proyecto detectado: {project_root}")

try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash
except ImportError as e:
    print(f"❌ Error de importación crítico: {e}")
    print("🔍 sys.path actual:", sys.path)
    sys.exit(1)

def create_admin():
    print("🔄 Conectando a la base de datos...")
    db = SessionLocal()
    try:
        # Buscar usuario trebolsoft
        user = db.query(User).filter(User.username == "trebolsoft").first()
        
        if user:
            print(f"✅ Usuario 'trebolsoft' encontrado (ID: {user.id}).")
            print("🔄 Actualizando permisos de Superusuario...")
            user.is_superuser = True
            user.is_active = True
        else:
            print(f"🆕 Usuario 'trebolsoft' no existe. Creándolo ahora...")
            user = User(
                username="trebolsoft",
                email="admin@trebolsoft.com",
                hashed_password=get_password_hash("Admin123!"),
                is_active=True,
                is_superuser=True
            )
            db.add(user)
        
        db.commit()
        print("🚀 ¡ÉXITO! El usuario 'trebolsoft' ahora es Administrador en DigitalOcean.")
        
    except Exception as e:
        print(f"❌ Error operando en base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
