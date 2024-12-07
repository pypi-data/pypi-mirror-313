from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

env = os.getenv("ENV", "qa")
if env == "qa":
    load_dotenv(".env.qa")
elif env == "production":
    load_dotenv(".env.production")
elif env == "pc":
    load_dotenv(".env.pc")


print("*" * 100)
print(f"ENVIRONMENT: {os.getenv('APP_ENVIRONMENT')}")
print(f"PROJECT_NAME: {os.getenv('PROJECT_NAME')}")
print(f"PROJECT_VERSION: {os.getenv('PROJECT_VERSION')}")
print(f"HAS_TRACK: {os.getenv('HAS_TRACK')}")
print("*" * 100)


class Settings(BaseSettings):
    app_name: str = "Platform Management API"
    database_url: str = os.getenv("DATABASE_URL")
    database_user: str = os.getenv("DATABASE_USER")
    database_password: str = os.getenv("DATABASE_PASSWORD")
    database_name: str = os.getenv("DATABASE_NAME")
    database_host: str = os.getenv("DATABASE_HOST")
    secret_key: str = os.getenv("SECRET_KEY")
    has_debug: bool = os.getenv("HAS_DEBUG")
    has_track: bool = os.getenv("HAS_TRACK")
    project_version: str = os.getenv("PROJECT_VERSION")
    project_name: str = os.getenv("PROJECT_NAME")
    project_description: str = os.getenv("PROJECT_DESCRIPTION")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    app_environment: str = os.getenv("APP_ENVIRONMENT")
    api_platform: str = os.getenv("API_PLATFORM")

    class Config:
        env_file = ".env"


settings = Settings()
