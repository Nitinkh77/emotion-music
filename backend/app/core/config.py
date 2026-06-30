from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    youtube_api_key: str = ""
    cors_origins: str = "http://localhost:5173"
    max_image_size_mb: int = 5

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()