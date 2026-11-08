from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.users.schemas import UserCreate, UserResponse, UserUpdate
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    return await UserService.create_user(db, data)


@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[UserResponse]:
    return await UserService.get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    return await UserService.get_user(db, user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    return await UserService.update_user(db, user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await UserService.delete_user(db, user_id)
