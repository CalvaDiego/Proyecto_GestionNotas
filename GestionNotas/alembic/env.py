from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importar la configuración de la base de datos y los modelos
from CapaAccesoDatos.BaseDatos.models import *
from CapaAccesoDatos.BaseDatos.database import Base
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Cargar configuración de Alembic
config = context.config

# Establecer manualmente la URL de la base de datos desde el archivo .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Configuración de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData de los modelos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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