# Test_models = Tests unitaruis del modelo ML
# Fixtures para las pruebas (cliente TestClient, base de datos de prueba, etc)

import asyncio
from typing import AsyncGenerator
import pytest_lazyfixture
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from src.db.base import Base, get_db
from src.main import app
from src.core.security import hash_password, create_access_token
from src.db.base import User

@pytest.fixture(scope="session")
def engine():
    """Crea un motor SQLite asincrono en memoria (compartido entre tests)."""
    return create_async_engine("sqlite+aiosqlite://",
                            connect_args={"check_same_thread": False},
                            poolclass=StaticPool
                            )

@pytest.fixture(scope="session", autouse=True)
async def create_tables(engine):
    """Crea todas las tablas antes de ejecutar los tests y las eliimina al final."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Proporciona una sesion de base de datos aislada por test."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture(autouse=True)
async def override_dependency(db_session):
    """Reemplaza la dependencia get_db con nuestra sesion de prueba."""
    async def _get_test_db():
        yield db_session
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP asincrono para la aplicacion FastAPI de prueba."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# Fixtures de usuarios de prueba

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Crea un usuario de prueba y lo guarda en la DB."""
    user = User(email="test@example.com",
                hashed_password=hash_password("testpassword"),
                full_name="Test User",
                is_active=True
                )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return

@pytest.fixture
def test_token(test_user: User) -> str:
    """Genera un token JWT valido para el usuario de prueba."""
    return create_access_token(data={"sub": test_user.email})

@pytest.fixture
async def auth_client(async_client: AsyncClient, test_token: str) -> AsyncClient:
    """Cliente con cabecera de autorizacion ya configurada."""
    async_client.headers["Authorization"] = f"Bearer {test_token}"
    return async_client