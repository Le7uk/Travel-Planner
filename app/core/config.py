from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Travel Planner"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./travel_planner.db"
    auth_username: str = "admin"
    auth_password: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()
