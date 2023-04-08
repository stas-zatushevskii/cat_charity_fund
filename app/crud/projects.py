from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDProjects(CRUDBase):
    async def get_projects_by_name(
        self,
        name: str,
        session: AsyncSession
    ):
        return await session.scalar(
            select(CharityProject).where(
                CharityProject.name == name
            )
        )


projects_crud = CRUDProjects(CharityProject)