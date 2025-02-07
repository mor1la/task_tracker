from fastapi import APIRouter, HTTPException, Response
from app.role.DTO import RoleCreateDTO, RoleUpdateDTO
from app.role.service import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_role(role: RoleCreateDTO):
    result = await RoleService.create_role(
        name=role.name, description=role.description
    )
    return result


@router.get("/")
async def get_all_roles():
    result = await RoleService.get_all_roles()
    return result


@router.put("/{role_id}")
async def update_role(role_id: int, role: RoleUpdateDTO):
    await RoleService.update_role(
        role_id=role_id, name=role.name, description=role.description
    )
    return {"detail": "Role updated successfully"}
