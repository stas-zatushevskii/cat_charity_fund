from pydantic import BaseSettings
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'FIRST_SUPERUSER_EMAIL'
    first_superuser_password: Optional[str] = 'FIRST_SUPERUSER_PASSWORD'

    class Config:
        env_file = '.env'


settings = Settings()
