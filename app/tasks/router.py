from fastapi import APIRouter, HTTPException, Depends
from app.tasks.DTO import TaskCreateDTO, TaskUpdateDTO, TaskDTO
from app.tasks.service import TaskService
from app.tasks.schemas import TaskResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session_maker

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@router.post("/", response_model=TaskResponseSchema)
async def create_task(task: TaskCreateDTO, session: AsyncSession = Depends(get_async_session)):
    return await TaskService.create_task(task.title, task.description, task.created_at, task.project_id, task.assignee_id)

@router.get("/{task_id}", response_model=TaskDTO)
async def get_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    return await TaskService.get_task_by_id(task_id)

@router.put("/{task_id}", response_model=TaskDTO)
async def update_task(task_id: int, task: TaskUpdateDTO, session: AsyncSession = Depends(get_async_session)):
    return await TaskService.update_task(task_id, task)

@router.delete("/{task_id}")
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    await TaskService.delete_task(task_id)
    return {"detail": "Task deleted successfully"}
