# Migraciones de base de datos con Alembic para el proyecto ML FastAPI
# Este es el fichero más importante. Configura la conexión asíncrona y carga los metadatos de nuestros modelos.

import asyncio
import os
import logging
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Importamos nuestra metadata de modelos para que Alembic pueda detectar los cambios
from src.db.base import Base
from src.core.config import settings

logging.basicConfig(level=logging.INFO)

# Configuración de logging de Alembic
config = context.config


# Sobrescribimos la URL de la base de datos con la de settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# MetaData que incluye todas las tablas de nuestros modelos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo offline (sin conexion a BD)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """Ejecuta las migraciones en modo online (con conexion a BD)."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Crea un engine asincrono y ejecuta las migraciones."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo online usando asyncio con DB real."""
    asyncio.run(run_async_migrations())

# Elegir modo offline u online segun contexto
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()