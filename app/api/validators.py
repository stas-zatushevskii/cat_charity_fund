from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import projects_crud
from app.models import CharityProject
from app.schemas.projects import ProjectsUpdate


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await projects_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найдена!'
        )
    return project


async def check_name(
        name: str,
        session: AsyncSession,
) -> CharityProject:
    name_db = await projects_crud.get_projects_by_name(name, session)
    if name_db is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_full_amount(
        full_amount: int,
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await projects_crud.get(project_id, session)
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    if full_amount < project.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже вложенной'
        )
    return project


async def check_project_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await projects_crud.get(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_charity_project_before_update(
    charity_project_id: int,
    charity_project_in: ProjectsUpdate,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await check_project_exists(
        project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    full_amount_update_value = charity_project_in.full_amount
    if (full_amount_update_value and
       charity_project.invested_amount > full_amount_update_value):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую cумму меньше уже вложенной'
        )
    name_update_value = charity_project_in.name
    await check_name(
        name=name_update_value, session=session
    )
    return charity_project
