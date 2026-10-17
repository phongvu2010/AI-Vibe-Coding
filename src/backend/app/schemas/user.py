import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Schema cơ sở chia sẻ chung các thuộc tính User (chuẩn 100% snake_case)"""
    email: EmailStr = Field(..., description="Địa chỉ email hợp lệ")
    full_name: str = Field(..., min_length=1, max_length=255, description="Họ và tên đầy đủ")
    is_active: bool = Field(default=True, description="Trạng thái kích hoạt tài khoản")

class UserCreate(UserBase):
    """Schema tiếp nhận dữ liệu khi tạo mới User"""
    pass

class UserUpdate(BaseModel):
    """Schema cập nhật thông tin User"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """Schema dữ liệu trả về cho Client - Khớp chính xác với TypeScript Interface"""
    id: uuid.UUID = Field(..., description="Khóa chính định danh UUID")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    model_config = ConfigDict(from_attributes=True)
