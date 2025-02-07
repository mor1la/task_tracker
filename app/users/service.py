from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import select, insert, delete

from app.db import async_session_maker
from app.exceptions import USER_ALREADY_EXISTS, USER_BAD_LOGIN
from app.users.auth import cypher_password, check_password, create_jwt_token
from app.users.model import Users
from sqlalchemy.ext.asyncio import AsyncSession

from app.organizations.model import Organization


class UserService:
    model = Users

    @classmethod
    async def create_user(cls, email: str, password: str, username: str) -> Users:
        async with async_session_maker() as session:
            await cls.check_if_user_exists(session, email)
            await cls.add_user(session, email, password, username)

            user = await cls.find_user_by_email(email)

            return user

    @classmethod
    async def add_user(cls, session: AsyncSession, email: str, password: str, username: str,
                       role_id: Optional[int] = None):
        hashed_password = cypher_password(password)
        query = insert(cls.model).values(
            email=email,
            username=username,
            password=hashed_password,
            role_id=role_id
        )
        await session.execute(query)
        await session.commit()

    @classmethod
    async def check_if_user_exists(cls, session: AsyncSession, email: str) -> None:
        user = await cls.find_user_by_email(email)
        if user:
            raise USER_ALREADY_EXISTS

    @classmethod
    async def find_user_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.email == email)
            return (await session.execute(query)).scalar_one_or_none()
    @classmethod
    async def login_user(cls, email: str, password: str):
        async with async_session_maker() as session:
            user = await cls.find_user_by_email(email)
            if not user:
                raise USER_BAD_LOGIN
            is_correct_password = check_password(password, user.password)
            if not is_correct_password:
                raise USER_BAD_LOGIN
            token = create_jwt_token({"sub": email})
            return token

    @classmethod
    async def update_user_organizations(cls, session: AsyncSession, user_id: int, organization_ids: List[int]):
        await session.execute(
            delete(Organization)
            .where(Organization.user_id == user_id)
        )

        if not organization_ids:
            await session.commit()
            return

        insert_queries = [
            insert(Organization).values(user_id=user_id, organization_id=org_id) for org_id in organization_ids
        ]

        for query in insert_queries:
            await session.execute(query)

        await session.commit()
