from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Agregar el directorio raíz al PYTHONPATH para importar app
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Importar settings para inyectar la URL de DB en Alembic
from app.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Forzar que Alembic use la URL de base de datos del entorno (Render)
if settings.database_url:
    config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from app.core.database import Base
# target_metadata = Base.metadata

# --- INICIO DE LA CONFIGURACIÓN PARA AUTOGENERATE ---
# Importar la Base de SQLAlchemy desde nuestra aplicación
from app.core.database import Base

# Importar todos los modelos para que Alembic los reconozca
from app.models.user import User
from app.models.client import Client
from app.models.credit import Credit
from app.models.payment import Payment
from app.models.cash_transaction import CashTransaction
from app.models.box import Box, BoxMovement

# Asignar la metadata de nuestros modelos a Alembic
target_metadata = Base.metadata
# --- FIN DE LA CONFIGURACIÓN PARA AUTOGENERATE ---


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
