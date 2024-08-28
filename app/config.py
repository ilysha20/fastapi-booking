from pydantic import model_validator, BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # db config
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str | None = None

    @model_validator(mode='before')
    @classmethod
    def assemble_database_url(cls, values):
        values["DATABASE_URL"] = f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASSWORD']}@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        return values

    # jwt config
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'

settings = Settings()
