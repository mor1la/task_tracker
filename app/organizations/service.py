from sqlalchemy import select, insert, update
from fastapi import HTTPException

from app.db import async_session_maker
from app.exceptions import ORGANIZATION_ALREADY_EXISTS, ORGANIZATION_NOT_FOUND
from app.organizations.model import Organization
from app.users.model import Users

from app.users.model import UserOrganizations

from app.users.service import UserService

from app.role.model import RoleEnum

from app.Notifications import NotificationsAlert
from app.messages import *

from app.messages import COMPANY_TEXT, COMPANY_HTML, HIRE_EMPLOYEE_TEXT, HIRE_EMPLOYEE_HTML


class OrganizationService:

    model = Organization

    @classmethod
    async def create_organization(cls, name: str, description: str, user_email: str) -> Organization:
        async with async_session_maker() as session:
            await cls.check_if_organization_exists(session, name)
            await cls.add_organization(session, name, description)
            organization = await cls.find_organization_by_name(session, name)
            await cls.update_users_organization(session, organization.id, user_email)
            await cls.assign_role_to_user(session, user_email, RoleEnum.CREATOR)
            NotificationsAlert.send_email(user_email, "Организация создана", COMPANY_TEXT, COMPANY_HTML)
            return organization

    @classmethod
    async def add_organization(cls, session, name: str, description: str):
        query = insert(cls.model).values(name=name, description=description)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def check_if_organization_exists(cls, db_session, name: str) -> None:
        organization = await cls.find_organization_by_name(db_session, name)
        if organization:
            raise ORGANIZATION_ALREADY_EXISTS

    @classmethod
    async def find_organization_by_name(cls, session, name):
        query = select(cls.model).where(cls.model.name == name)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def assign_role_to_user(cls, session, user_email: str, role: RoleEnum):
        user = await UserService.find_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        query = (
            update(Users)
            .where(Users.id == user.id)
            .values(role_id=role.value)
        )
        await session.execute(query)
        await session.commit()

    @classmethod
    async def update_users_organization(cls, session, organization_id: int, user_email: str):
        user = await UserService.find_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        query = insert(UserOrganizations).values(user_id=user.id, organization_id=organization_id)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def update_organization(cls, organization_id: int, name: str, description: str):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == organization_id)
                .values(name=name, description=description)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_organizations_by_ids(cls, session, organization_ids):
        if not organization_ids:
            return []

        query = select(cls.model).where(cls.model.id.in_(organization_ids))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_all_organizations(cls, user_email: str):
        async with async_session_maker() as session:
            user = await UserService.find_user_by_email(user_email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Explicitly query for user's organizations to avoid lazy loading issues
            query = select(UserOrganizations).where(UserOrganizations.user_id == user.id)
            user_organizations = await session.execute(query)
            organization_ids = [uo.organization_id for uo in user_organizations.scalars()]

            if not organization_ids:
                return []

            result = await cls.get_organizations_by_ids(session, organization_ids)
            return result
    @classmethod
    async def add_worker_to_organization(cls, organization_id: int, user_email: str):
        async with async_session_maker() as session:
            user = await UserService.find_user_by_email(user_email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Проверяем, существует ли организация
            organization = await cls.find_organization_by_id(session, organization_id)
            if not organization:
                raise HTTPException(status_code=404, detail="Organization not found")

            # Добавляем работника в организацию
            query = insert(UserOrganizations).values(user_id=user.id, organization_id=organization.id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_organization_by_id(cls, session, organization_id: int):
        query = select(cls.model).where(cls.model.id == organization_id)
        return (await session.execute(query)).scalar_one_or_none()