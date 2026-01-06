import os
from pydantic_settings import BaseSettings


### JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

### DB Configuration
DB_USER = os.getenv("DB_USER", "receipt_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "receipt_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "receipt_app")

### OTP Configuration
OTP_EXPIRY_MINUTES = 5



class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    JWT_SECRET_KEY: str
    OCR_MODE: str = "mock"

    class Config:
        env_file = ".env"  # Will be overridden by Docker

settings = Settings()