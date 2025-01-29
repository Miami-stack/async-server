from src.db.db import SessionLocal


async def get_db():
    async with SessionLocal() as db:
        yield db
        await db.commit()
