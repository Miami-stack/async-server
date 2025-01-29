
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import app_settings

DATABASE_URL = app_settings.DATABASE_DSN

engine = create_async_engine(DATABASE_URL, echo=app_settings.ECHO, future=True)
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)