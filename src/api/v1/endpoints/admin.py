from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.base import User
from src.db.session import get_db
from src.api.v1.dependencies import get_current_user
from src.services.prediction_service import load_model

router = APIRouter(tags=["admin"])

@router.post(".retrain", status_code=202)
async def retrain_model(current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    """Reentrena el modelo (solo para administradores)."""
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Se requieren privilegios de administrador para realizar esta acción.")

    try:
        import subprocess
        import sys
        result = subprocess.run([sys.executable, "scripts/train_model.py"], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        load_model()
        return {"message": "Modelo reencontrado exitosamente", "details": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error en reentrenamiento del modelo: {str(e)}")
    