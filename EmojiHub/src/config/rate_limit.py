from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    rate_limit: str = Field("5/second", alias="RATE_LIMIT", description="[count] [per|/] [n (optional)] [second|minute|hour|day|month|year]")


settings = Settings()
