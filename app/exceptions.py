from fastapi import HTTPException

USER_ALREADY_EXISTS = HTTPException(status_code=401, detail="User with this email already exists")
USER_BAD_LOGIN = HTTPException(status_code=400, detail="Incorrect email or password")
ORGANIZATION_ALREADY_EXISTS = HTTPException(status_code=400, detail="Organization already exists.")
ORGANIZATION_NOT_FOUND = HTTPException(status_code=404, detail="Organization not found.")
TASK_STATUS_ALREADY_EXISTS = HTTPException(status_code=400, detail="Task status already exists.")
TASK_STATUS_NOT_FOUND = HTTPException(status_code=404, detail="Task status not found.")
PROJECT_ALREADY_EXISTS = HTTPException(status_code=400, detail="Project already exists.")
PROJECT_NOT_FOUND = HTTPException(status_code=404, detail="Project not found.")
ROLE_ALREADY_EXISTS = HTTPException(status_code=400, detail="Role already exists.")
ROLE_NOT_FOUND = HTTPException(status_code=404, detail="Role not found.")
