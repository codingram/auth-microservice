from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
	SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
	DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
	ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

	class Config:
		env_file = ".env"


settings = Settings()
