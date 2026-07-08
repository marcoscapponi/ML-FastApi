# Funciones de seguridad: hash de contrasenias y manejo de tokens JWT

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """Trunca una contrasenia a un maximo de bytes para evitar problemas con bcrypt."""
    encoded = password.encode('utf-8')
    if len(encoded) <= max_bytes:
        return password
    return encoded[:max_bytes].decode('utf-8', errors='ignore')

def hash_password(password: str) -> str:
    """Devuelve el hash de la contrasenia en texto plano"""
    truncated_password = _truncate_password(password)
    return pwd_context.hash(truncated_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contrasenia en texto plano coincida con el hash"""
    truncated_password = _truncate_password(plain_password)
    return pwd_context.verify(truncated_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un token JWT con los datos proporcionados.
        'data' tipicamente contiene 'sub' (subject, el email del usuario)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    """Decodifica un token JWT y devuelve el payload.
        Retorna Nonoe si el token es invalido o ha expirado."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None