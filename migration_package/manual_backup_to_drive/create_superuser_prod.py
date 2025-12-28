import sys
import os

# --- CONFIGURACIÓN DE RUTA ROBUSTA ---
current_script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(current_script_path)
# Ajustar según profundidad: migration_package/manual_backup_to_drive/ -> ../../..
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_script_path)))
sys.path.insert(0, project_root)

try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash
except ImportError:
    # Fallback por si la estructura de carpetas es diferente al ejecutar
    sys.path.insert(0, os.getcwd())
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash

def create_admin():
    print("🔄 Conectando a la base de datos...")
    db = SessionLocal()
    try:
        # 1. Buscar si el usuario ya existe
        user = db.query(User).filter(User.username == "trebolsoft").first()
        
        if user:
            print(f"✅ Usuario 'trebolsoft' encontrado.")
            print("🔄 Actualizando permisos de Superusuario...")
            user.is_superuser = True
            user.is_active = True
        else:
            print(f"🆕 Usuario 'trebolsoft' no existe. Creándolo...")
            # Usar variable de entorno o valor por defecto seguro
            admin_pass = os.getenv("ADMIN_PASSWORD", "Admin123!")
            user = User(
                username="trebolsoft",
                email="admin@trebolsoft.com",
                hashed_password=get_password_hash(admin_pass),
                is_active=True,
                is_superuser=True
            )
            db.add(user)
        
        db.commit()
        print("🚀 ¡ÉXITO! Permisos de administrador actualizados.")
        
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
