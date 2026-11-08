from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: TaskCreate,
    ) -> Task:
        task = Task(
            request_id=data.request_id,
            assigned_to=data.assigned_to,
            title=data.title,
            description=data.description,
            priority=data.priority,
            due_date=data.due_date,
        )

        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        task_id: int,
    ) -> Task | None:
        result = await db.execute(select(Task).where(Task.id == task_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Task]:
        result = await db.execute(select(Task).order_by(Task.id))

        return list(result.scalars().all())

    @staticmethod
    async def get_by_request_id(
        db: AsyncSession,
        request_id: int,
    ) -> list[Task]:
        result = await db.execute(
            select(Task).where(Task.request_id == request_id).order_by(Task.id)
        )

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        task: Task,
        data: TaskUpdate,
    ) -> Task:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        await db.commit()
        await db.refresh(task)

        return task

    @staticmethod
    async def delete(
        db: AsyncSession,
        task: Task,
    ) -> None:
        await db.delete(task)
        await db.commit()
