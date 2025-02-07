from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy import select

from app.db import async_session_maker
from app.users.DTO import UserRegisterDTO, UserLoginDTO
from app.users.auth import verify_jwt_token, get_user_email_by_token
from app.users.model import Users
from app.users.service import UserService
from sqlalchemy.orm import selectinload

from app.role.service import RoleService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    async with async_session_maker() as session:
        result = await session.execute(
            select(Users).options(selectinload(Users.organizations))
        )
        users = result.scalars().all()

        response = []
        for user in users:
            role_name = await RoleService.get_role_name_by_id(user.role_id) if user.role_id else "No role"
            response.append({
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": role_name,
                "organization_ids": [org.id for org in user.organizations]
            })

        return response


@router.post("/register")
async def register_user(user: UserRegisterDTO):
    result = await UserService.create_user(
        email=user.email,
        password=user.password,
        username=user.username,
    )
    return result



@router.post("/login")
async def login_user(response: Response, user: UserLoginDTO):
    result = await UserService.login_user(email=user.email, password=user.password)
    response.set_cookie(key="token", value=result, httponly=True)
    return {"detail": "Success"}


@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="token")
    return {"detail": "Success"}


@router.get("/me")
async def return_user(user_email: str = Depends(get_user_email_by_token)):
    return user_email
