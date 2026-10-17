import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.app.schemas.user import UserCreate, UserResponse
from src.backend.app.services.user_service import UserService
from src.db.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Lấy danh sách người dùng phân trang"""
    service = UserService(db)
    return await service.get_all_users(skip=skip, limit=limit)

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Tạo mới một người dùng"""
    service = UserService(db)
    return await service.create_user(payload)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Lấy chi tiết một người dùng theo ID"""
    service = UserService(db)
    return await service.get_user_by_id(user_id)
