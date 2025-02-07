from fastapi import APIRouter, HTTPException, Response, Depends
from app.organizations.DTO import OrganizationCreateDTO, OrganizationUpdateDTO
from app.organizations.service import OrganizationService
from app.users.auth import get_user_email_by_token

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_organization(organization: OrganizationCreateDTO, user_email: str = Depends(get_user_email_by_token)):
    result = await OrganizationService.create_organization(
        name=organization.name, description=organization.description, user_email=user_email
    )
    return result

@router.get("/")
async def get_all_organizations(user_email: str = Depends(get_user_email_by_token)):
    result = await OrganizationService.get_all_organizations(user_email)
    return result

@router.put("/{organization_id}")
async def update_organization(organization_id: int, organization: OrganizationUpdateDTO):
    await OrganizationService.update_organization(
        organization_id=organization_id, name=organization.name, description=organization.description
    )
    return {"detail": "Organization updated successfully"}

@router.post("/{organization_id}/add_worker")
async def add_worker_to_organization(organization_id: int, user_email: str):
    await OrganizationService.add_worker_to_organization(organization_id, user_email)
    return {"detail": "Worker added to organization successfully"}

