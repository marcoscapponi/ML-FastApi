from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.schemas.user import UserCreate, UserResponse, UserLogin
from src.schemas.token import Token
from src.services.auth_service import authenticate_user, register_user

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Registra un nuevo usuario."""
    user = await register_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Inicia sesion y devuelve un token JWT."""
    return await authenticate_user(db, login_data) 