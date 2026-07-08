#Pydantic schemas (dominio y responses) relacionados a usuarios

from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, man_length=12)
    full_name: str | None = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
    is_active: bool
    model_config = {"from_attributes": True} # Permite convertir de ORM a Pydantic

class UserLogin(BaseModel):
    email: EmailStr
    password: str