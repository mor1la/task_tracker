from fastapi import APIRouter, HTTPException
from app.task_status.DTO import TaskStatusCreateDTO, TaskStatusUpdateDTO
from app.task_status.service import TaskStatusService

router = APIRouter(
    prefix="/task-statuses",
    tags=["task-statuses"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_all_task_statuses():
    return await TaskStatusService.list_all_task_statuses()

@router.post("/")
async def create_task_status(task_status: TaskStatusCreateDTO):
    try:
        return await TaskStatusService.create_task_status(
            name=task_status.name,
            description=task_status.description
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{task_status_id}")
async def update_task_status(task_status_id: int, task_status: TaskStatusUpdateDTO):
    try:
        return await TaskStatusService.update_task_status(
            task_status_id=task_status_id,
            name=task_status.name,
            description=task_status.description
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{task_status_id}")
async def delete_task_status(task_status_id: int):
    try:
        await TaskStatusService.delete_task_status(task_status_id)
        return {"detail": "Task status deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))