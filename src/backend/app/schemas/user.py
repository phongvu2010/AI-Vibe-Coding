import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

try:
    import email_validator  # noqa: F401
    from pydantic import EmailStr
except ImportError:
    # Fallback to string with regex when email-validator is not installed
    EmailStr = Annotated[str, StringConstraints(pattern=r"^[^@]+@[^@]+\.[^@]+$")]  # type: ignore


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
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None

class UserResponse(UserBase):
    """Schema dữ liệu trả về cho Client - Khớp chính xác với TypeScript Interface"""
    id: uuid.UUID = Field(..., description="Khóa chính định danh UUID")
    created_at: datetime = Field(..., description="Thời gian tạo bản ghi")
    updated_at: datetime = Field(..., description="Thời gian cập nhật bản ghi")

    model_config = ConfigDict(from_attributes=True)
