from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_tables
from app.users.router import router as users_router
from app.organizations.router import router as organizations_router
from app.project.router import router as project_router
from app.role.router import router as roles_router
from app.tasks.router import router as tasks_router
from app.task_status.router import router as task_status_router

app = FastAPI()

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники (можно заменить на список конкретных источников)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, etc.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(project_router)
app.include_router(roles_router)
app.include_router(tasks_router)
app.include_router(task_status_router)

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}