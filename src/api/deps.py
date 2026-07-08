"""Dependencias comunes para todos los routers."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import async_session_factory

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session