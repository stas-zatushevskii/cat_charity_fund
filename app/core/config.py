from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'STAs20160@yandex.ru'
    first_superuser_password: Optional[str] = '123321123'

    class Config:
        env_file = '.env'


settings = Settings()
