from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

CREATED_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

CLOSED_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ProjectsCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Мощный котик',
                'description': 'Создаем фитнесс-центр',
                'full_amount': 500
            }
        }


class ProjectsUpdate(BaseModel):

    name: Optional[str] = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Мощный котик',
                'description': 'Создаем фитнесс-центр',
                'full_amount': 500
            }
        }


class ProjectsDB(ProjectsCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
