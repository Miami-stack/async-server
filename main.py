import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.files import file_router
from src.api.v1.users import user_router
from src.api.v1.healtcheck import router
from src.core.config import app_settings
from src.db.db import engine
from src.models.models_database import Base

app = FastAPI(
    title="load_files",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router)
app.include_router(user_router)
app.include_router(file_router)

if __name__ == "__main__":
    uvicorn.run(app, host=app_settings.HOST, port=app_settings.PORT)

