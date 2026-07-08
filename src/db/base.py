# Configuracion de la base de datos asincrona y modelos de SQLAlchemy

from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings  

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, 
                            echo=False, 
                            future=True)

async_session_factory = async_sessionmaker(engine,
                                        class_=AsyncSession,
                                        expire_on_commit=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_admin = Column(Boolean, default=False, server_default=('false'))
    
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    input_data = Column(JSON, nullable=False)
    predicted_class = Column(Integer, nullable=True)
    probability = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class_name = Column(String(50), nullable=True, default='')
    sepal_length = Column(Float, nullable=True, default=0.0)
    sepal_width = Column(Float, nullable=True, default=0.0)
    petal_length = Column(Float, nullable=True, default=0.0)
    petal_width = Column(Float, nullable=True, default=0.0)

    user = relationship("User", back_populates="predictions")