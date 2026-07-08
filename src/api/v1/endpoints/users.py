from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import User
from src.db.session import get_db
from src.schemas.user import UserResponse
from src.api.v1.dependencies import get_current_user
from src.services.user_service import get_user_profile

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """Obtiene el perfil del usuario autenticado."""
    return UserResponse.model_validate(current_user)