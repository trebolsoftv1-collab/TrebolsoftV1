import sys
import os

# --- CONFIGURACIÓN DE RUTA ---
current_script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(current_script_path)
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

print(f"📂 Raíz del proyecto: {project_root}")

# --- DIAGNÓSTICO DE ERRORES COMUNES ---
# 1. Verificar si existe un archivo app.py que cause conflicto
conflict_file = os.path.join(project_root, "app.py")
if os.path.exists(conflict_file):
    print("\n⚠️  ¡CONFLICTO DETECTADO!")
    print(f"   Existe un archivo '{conflict_file}' que impide importar la carpeta 'app'.")
    print("   👉 SOLUCIÓN: Renombra ese archivo a 'main.py' o 'run.py' en el servidor.")
    print("      Comando sugerido: mv app.py main.py")
    sys.exit(1)

# 2. Verificar estructura básica
if not os.path.isdir(os.path.join(project_root, "app")):
    print(f"\n❌ Error: No se encuentra la carpeta 'app' en {project_root}")
    print("   Contenido actual:", os.listdir(project_root))
    sys.exit(1)

try:
    from app.core.database import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash
except ImportError as e:
    print(f"\n❌ Error de importación: {e}")
    print("   Verifica que exista 'app/core/database.py'")
    sys.exit(1)

def create_admin():
    print("🔄 Conectando a la base de datos...")
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
        print("🚀 ¡ÉXITO! Usuario administrador configurado correctamente en DigitalOcean.")
        
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
