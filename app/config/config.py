from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    JWT_SECRET_KEY: str
    OCR_MODE: str = "mock"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"  # Will be overridden by Docker

settings = Settings()