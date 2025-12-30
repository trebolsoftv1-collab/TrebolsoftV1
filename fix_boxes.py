import sys
import os

# Aseguramos que Python encuentre la carpeta 'app'
sys.path.append(os.getcwd())

from app.core.database import SessionLocal
from app.models.user import User
from app.crud.box import create_box, get_box_by_user_id

def main():
    db = SessionLocal()
    try:
        print("--- Iniciando creación de cajas para usuarios existentes ---")
        users = db.query(User).all()
        count = 0
        for user in users:
            # Verificar si el usuario ya tiene caja
            if not get_box_by_user_id(db, user.id):
                print(f"Creando caja para usuario: {user.username}")
                create_box(db, user.id)
                count += 1
            else:
                print(f"Usuario {user.username} ya tiene caja.")
        
        print(f"--- Proceso terminado. Se crearon {count} cajas nuevas. ---")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()

