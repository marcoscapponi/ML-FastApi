# Punto de entrada principal para la aplicación FastAPI de ejemplo con ML

"""Aplicacion principal de FastApi."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.router import api_v1_router
from src.core.config import settings
from src.services.prediction_service import load_model
from src.core.exceptions import http_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de inicio y cierre de la aplicacion."""
    load_model()
    yield

app = FastAPI(
    title="ML API con FastAPI",
    description="API para clasificacion con modelo ML, autenticacion JWT y base de datos PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["health"])
async def root():
    return {"message": "ML API funcionando. Visita /docs para la documentacion."}