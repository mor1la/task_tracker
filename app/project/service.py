from sqlalchemy import select, insert, update
from fastapi import HTTPException

from app.db import async_session_maker
from app.exceptions import PROJECT_ALREADY_EXISTS, PROJECT_NOT_FOUND, ORGANIZATION_NOT_FOUND
from app.project.model import Project
from app.organizations.model import Organization
from sqlalchemy.ext.asyncio import AsyncSession


class ProjectService:

    model = Project

    @classmethod
    async def create_project(cls, name: str, description: str, organization_id: int, creator_id: int,
                             session: AsyncSession):
        new_project = Project(name=name, description=description, organization_id=organization_id,
                              creator_id=creator_id)
        session.add(new_project)
        await session.commit()
        return new_project

    @classmethod
    async def add_project(cls, name: str, description: str, organization_id: int, creator_id: int):
        async with async_session_maker() as session:
            query = insert(cls.model).values(name=name, description=description, organization_id=organization_id,
                                             creator_id=creator_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def check_if_project_exists(cls, name: str, session) -> None:
        project = await cls.find_project_by_name(name, session)
        if project:
            raise PROJECT_ALREADY_EXISTS

    @classmethod
    async def check_if_organization_exists(cls, organization_id: int, session) -> None:
        query = select(Organization).where(Organization.id == organization_id)
        organization = (await session.execute(query)).scalar_one_or_none()
        if not organization:
            raise ORGANIZATION_NOT_FOUND

    @classmethod
    async def find_project_by_name(cls, name: str, session):
        query = select(cls.model).where(cls.model.name == name)
        return (await session.execute(query)).scalar_one_or_none()

    @classmethod
    async def update_project(cls, project_id: int, name: str, description: str, session: AsyncSession):
        project = await session.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        project.name = name
        project.description = description
        await session.commit()

    @classmethod
    async def get_all_projects(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            return (await session.execute(query)).scalars().all()
