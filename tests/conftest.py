import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.models.models_database import Base
from src.services.db_service import get_db

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/database"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


async def override_get_db():
    async with TestingSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://localhost:8080") as ac:
        yield ac


@pytest.fixture
async def test_db():
    async with TestingSessionLocal() as db:
        yield db
