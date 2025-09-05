"""Application settings configuration."""

from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = config("DATABASE_URL")
    test_database_url: str = config("TEST_DATABASE_URL", default="")
    
    # Redis
    redis_url: str = config("REDIS_URL")
    
    # JWT
    secret_key: str = config("SECRET_KEY")
    algorithm: str = config("ALGORITHM", default="HS256")
    access_token_expire_minutes: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", 
        default=30, 
        cast=int
    )
    
    # External APIs
    dog_ceo_api_url: str = config(
        "DOG_CEO_API_URL", 
        default="https://dog.ceo/api/breeds/image/random"
    )
    
    # Environment
    environment: str = config("ENVIRONMENT", default="development")
    
    # CORS
    allowed_origins: list = ["*"]
    allowed_methods: list = ["*"]
    allowed_headers: list = ["*"]
    
    class Config:
        """Pydantic config."""
        env_file = ".env"


settings = Settings()