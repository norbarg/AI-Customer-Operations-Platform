from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserUpdate


class UserService:
    @staticmethod
    async def create_user(
        db: AsyncSession,
        data: UserCreate,
    ) -> User:
        existing_user = await UserRepository.get_by_email(
            db,
            data.email,
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        return await UserRepository.create(db, data)

    @staticmethod
    async def get_user(
        db: AsyncSession,
        user_id: int,
    ) -> User:
        user = await UserRepository.get_by_id(db, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    @staticmethod
    async def get_users(
        db: AsyncSession,
    ) -> list[User]:
        return await UserRepository.get_all(db)

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        data: UserUpdate,
    ) -> User:
        user = await UserService.get_user(db, user_id)

        if data.email is not None and data.email != user.email:
            existing_user = await UserRepository.get_by_email(
                db,
                data.email,
            )

            if existing_user is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User with this email already exists",
                )

        return await UserRepository.update(db, user, data)

    @staticmethod
    async def delete_user(
        db: AsyncSession,
        user_id: int,
    ) -> None:
        user = await UserService.get_user(db, user_id)
        await UserRepository.delete(db, user)
