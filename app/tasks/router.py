from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.tasks.service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    return await TaskService.create_task(db, data)


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def get_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    request_id: Annotated[int | None, Query()] = None,
) -> list[TaskResponse]:
    return await TaskService.get_tasks(db, request_id)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    return await TaskService.get_task(db, task_id)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaskResponse:
    return await TaskService.update_task(db, task_id, data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await TaskService.delete_task(db, task_id)
