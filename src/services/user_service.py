"""Servicio de usuarios: perfil, etc."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from src.db.base import User
from src.schemas.user import UserResponse

async def get_user_profile(db: AsyncSession, user: User) -> UserResponse:
    """Devuelve el perfil del usuario autenticado."""
    return UserResponse.model_validate(user)