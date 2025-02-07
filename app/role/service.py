from fastapi import HTTPException
from sqlalchemy import select
from app.db import async_session_maker
from app.role.model import Role, RoleEnum
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ROLE_NOT_FOUND


class RoleService:

    @classmethod
    async def get_all_roles(cls):
        return [{"name": role.name, "value": role.value} for role in RoleEnum]

    @classmethod
    async def get_role_name_by_id(cls, role_id: int) -> str:
        try:
            role = RoleEnum(role_id)
            return role.name
        except ValueError:
            return "Unknown role"