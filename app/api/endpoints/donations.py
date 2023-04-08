from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donatons_crud
from app.models import User
from app.schemas.donations import DonationsCreate, DonationsDB
from app.services.investment_process import investment_process_donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationsDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude={'close_date'}
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    return await donatons_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationsDB,
    response_model_exclude_none=True,
    response_model_exclude={'fully_invested', 'invested_amount', 'user_id', 'close_date'}
)
async def create_new_donation(
        donation: DonationsCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    new_donate = await donatons_crud.create(donation, session, user)
    await investment_process_donation(new_donate, session=session)
    await session.refresh(new_donate)
    return new_donate


@router.get(
    '/my',
    response_model=Union[DonationsDB, list[DonationsDB]],
    response_model_exclude_none=True,
    response_model_exclude={'fully_invested', 'invested_amount', 'user_id'}
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    user_id = user.id
    return await donatons_crud.get_donations_by_id(user_id, session)