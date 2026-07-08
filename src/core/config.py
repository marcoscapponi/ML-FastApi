# Configuraciones y settings desde variables de entorno

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    MODEL_PATH: str = "src/models/artifacts/model.joblib"
    METADATA_PATH: str = "src/models/artifacts/metadata.json"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:8000", "http://localhost:3000"]
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

settings = Settings()

    