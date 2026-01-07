from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"

    DATABASE_URL: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE_DAYS: float

    class Config:
        env_file = ".env"  # Will be overridden by Docker

settings = Settings()