from typing import List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: Optional[str] = None
    apikeys: List[str] = []

    class Config:
        env_file = ".env"


settings = Settings()
