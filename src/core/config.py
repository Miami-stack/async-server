from pydantic import BaseSettings, PostgresDsn

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    DATABASE_DSN: PostgresDsn
    ECHO: bool
    HOST: str
    PORT: int

    class Config:
        env_file = ".env"


app_settings = Settings()
