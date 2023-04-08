from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_update,
                                check_name, check_project_exists,
                                check_project_invested_amount)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.projects import projects_crud
from app.schemas.projects import ProjectsCreate, ProjectsDB, ProjectsUpdate
from app.services.investment_process import investment_process_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[ProjectsDB],
    response_model_exclude_none=True,
)
async def get_all_projectss(
        session: AsyncSession = Depends(get_async_session),
):
    return await projects_crud.get_multi(session)


@router.post(
    '/',
    response_model=ProjectsDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_project(
        project: ProjectsCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name(project.name, session)
    new_project = await projects_crud.create(project, session)
    await investment_process_project(new_project, session=session)
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=ProjectsDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project_in: ProjectsUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project_db = await check_charity_project_before_update(
        charity_project_id=project_id,
        session=session,
        charity_project_in=charity_project_in
    )
    return await projects_crud.update(
        db_obj=charity_project_db, obj_in=charity_project_in, session=session
    )


@router.delete(
    '/{project_id}',
    response_model=ProjectsDB,
    dependencies=[Depends(current_superuser)],)
async def delete_reservation(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(
        project_id, session
    )
    project = await check_project_invested_amount(
        project_id, session
    )
    project = await projects_crud.remove(
        project, session
    )
    return project