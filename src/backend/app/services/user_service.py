import uuid
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.app.schemas.user import UserCreate
from src.db.models.user import User
from src.db.repositories.user_repository import UserRepository


class UserService:
    """Tầng xử lý logic nghiệp vụ Người Dùng"""
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy người dùng với mã ID: {user_id}"
            )
        return user

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.repo.get_all(skip=skip, limit=limit)

    async def create_user(self, payload: UserCreate) -> User:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{payload.email}' đã được sử dụng trong hệ thống."
            )
        new_user = User(
            email=payload.email,
            full_name=payload.full_name,
            is_active=payload.is_active
        )
        return await self.repo.create(new_user)
