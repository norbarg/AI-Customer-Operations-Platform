from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.requests.repository import RequestRepository
from app.tasks.models import Task
from app.tasks.repository import TaskRepository
from app.tasks.schemas import TaskCreate, TaskUpdate
from app.users.repository import UserRepository


class TaskService:
    @staticmethod
    async def create_task(
        db: AsyncSession,
        data: TaskCreate,
    ) -> Task:
        request = await RequestRepository.get_by_id(
            db,
            data.request_id,
        )

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        if data.assigned_to is not None:
            user = await UserRepository.get_by_id(
                db,
                data.assigned_to,
            )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assigned user not found",
                )

        return await TaskRepository.create(db, data)

    @staticmethod
    async def get_task(
        db: AsyncSession,
        task_id: int,
    ) -> Task:
        task = await TaskRepository.get_by_id(db, task_id)

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    @staticmethod
    async def get_tasks(
        db: AsyncSession,
        request_id: int | None = None,
    ) -> list[Task]:
        if request_id is not None:
            return await TaskRepository.get_by_request_id(
                db,
                request_id,
            )

        return await TaskRepository.get_all(db)

    @staticmethod
    async def update_task(
        db: AsyncSession,
        task_id: int,
        data: TaskUpdate,
    ) -> Task:
        task = await TaskService.get_task(db, task_id)

        if data.assigned_to is not None:
            user = await UserRepository.get_by_id(
                db,
                data.assigned_to,
            )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assigned user not found",
                )

        return await TaskRepository.update(
            db,
            task,
            data,
        )

    @staticmethod
    async def delete_task(
        db: AsyncSession,
        task_id: int,
    ) -> None:
        task = await TaskService.get_task(db, task_id)
        await TaskRepository.delete(db, task)
