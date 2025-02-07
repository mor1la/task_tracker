from fastapi import APIRouter, HTTPException, Response
from app.project.DTO import ProjectCreateDTO, ProjectUpdateDTO
from app.project.service import ProjectService

from app.db import async_session_maker

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create_project(project: ProjectCreateDTO):
    async with async_session_maker() as session:
        result = await ProjectService.create_project(
            name=project.name,
            description=project.description,
            organization_id=project.organization_id,
            creator_id=project.creator_id,
            session=session
        )
        return result


@router.put("/{project_id}")
async def update_project(project_id: int, project: ProjectUpdateDTO):
    async with async_session_maker() as session:
        await ProjectService.update_project(
            project_id=project_id,
            name=project.name,
            description=project.description,
            session=session
        )
        return {"detail": "Project updated successfully"}

