from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donations import donatons_crud
from app.crud.projects import projects_crud
from app.models import CharityProject, Donation


def fully_invest(obj: Union[CharityProject, Donation]) -> None:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investment_process_project(
        project: CharityProject,
        session: AsyncSession
):
    donations = await donatons_crud.not_fully_invested(
        session=session
    )

    for donation in donations:
        summ_need = project.full_amount - project.invested_amount
        if donation.full_amount > summ_need:
            donation.invested_amount += summ_need
            fully_invest(project)

        elif donation.full_amount <= summ_need:
            if donation.fully_invested is not True:
                fully_invest(donation)
                project.invested_amount += donation.invested_amount
                summ_need = summ_need - donation.full_amount
                if summ_need == 0:
                    fully_invest(project)

    await session.commit()


async def investment_process_donation(
        donation: Donation,
        session: AsyncSession
):
    projects = await projects_crud.not_fully_invested(
        session=session
    )

    for project in projects:
        summ_need = project.full_amount - project.invested_amount
        if donation.full_amount > summ_need:
            donation.invested_amount += summ_need
            fully_invest(project)

        elif donation.full_amount <= summ_need:
            if donation.fully_invested is not True:
                fully_invest(donation)
                project.invested_amount += donation.invested_amount
                summ_need = summ_need - donation.full_amount
                if summ_need == 0:
                    fully_invest(project)

    await session.commit()
