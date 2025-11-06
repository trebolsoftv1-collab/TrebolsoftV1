# Migración a PostgreSQL - Guía paso a paso
# migration_guide.md

## 🗄️ Cuándo migrar de SQLite a PostgreSQL

### ⚠️ INDICADORES CRÍTICOS:
- SQLite > 100MB
- Más de 1000 clientes en base de datos
- Múltiples usuarios simultáneos (>10)
- Errores de "database locked"

### 📋 PASOS DE MIGRACIÓN:

#### 1️⃣ Preparación (Antes de migrar):
```bash
# 1. Crear backup completo
python backup_script.py

# 2. Documentar estructura actual
sqlite3 dev.db ".schema" > current_schema.sql

# 3. Exportar datos
sqlite3 dev.db ".dump" > data_export.sql
```

#### 2️⃣ Configuración PostgreSQL en Render:
```python
# app/core/database.py - Nueva configuración

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Detectar tipo de base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    # PostgreSQL (Producción)
    engine = create_engine(DATABASE_URL)
else:
    # SQLite (Desarrollo)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./dev.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

#### 3️⃣ Migración de Datos:
```bash
# En servidor con PostgreSQL
pip install psycopg2-binary

# Convertir SQLite dump a PostgreSQL
python sqlite_to_postgres.py data_export.sql

# Importar a PostgreSQL
psql $DATABASE_URL < postgres_data.sql
```

#### 4️⃣ Validación:
```python
# Verificar migración
from app.core.database import SessionLocal
from app.models.user import User
from app.models.client import Client

db = SessionLocal()
print(f"Usuarios migrados: {db.query(User).count()}")
print(f"Clientes migrados: {db.query(Client).count()}")
```

### 💰 COSTOS:
- **SQLite**: $0 - incluido en plan actual
- **PostgreSQL**: $0 - incluido en Render Professional ($25/mes)
- **Tiempo migración**: 2-4 horas
- **Downtime**: 30-60 minutos

### 🛡️ BACKUP DURANTE MIGRACIÓN:
1. **NUNCA** migrar sin backup completo
2. Mantener SQLite como respaldo 48h
3. Probar aplicación completamente antes de eliminar SQLite
4. Tener plan de rollback preparado