from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/catfood_db"

    JWT_SECRET: str = "SUPER_SECRET_KEY"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()

