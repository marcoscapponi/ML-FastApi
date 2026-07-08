# api = Routers de FastAPI
# v1 = Versionado de la API
# Agrupa todas las rutas v1 

from fastapi import APIRouter
from src.api.v1.endpoints import users, predictions, auth, admin

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router, prefix="/auth")
api_v1_router.include_router(users.router, prefix="/users")
api_v1_router.include_router(predictions.router, prefix="/predictions")
api_v1_router.include_router(admin.router, prefix="/admin")