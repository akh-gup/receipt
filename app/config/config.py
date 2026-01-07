from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"

    # DB
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE_DAYS: float

    class Config:
        env_file = ".env"  # Will be overridden by Docker

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )
settings = Settings()