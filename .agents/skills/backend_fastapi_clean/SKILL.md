---
name: backend_fastapi_clean
description: "Guidelines for Clean Architecture with FastAPI, Pydantic v2 validation (strict snake_case), layered services & repositories, dependency injection, and standardized HTTP error responses in src/backend/."
---

# Backend Team Runbook: FastAPI + Pydantic v2 + Async Services (Clean Architecture)

Runbook này hướng dẫn `backend-dev` xây dựng REST API chất lượng cao, tuân thủ nghiêm ngặt **Cross-Layer Data Contract Matrix**, rào chắn an toàn dòng lệnh (**CLI Guardrails**) và tham gia vòng lặp tự sửa lỗi (**Feedback Loop**).

---

## 1. Rào Chắn An Toàn Dòng Lệnh (CLI Guardrails)
- **Quyền sở hữu**: Chỉ tạo/sửa file trong `src/backend/`.
- **Lệnh được phép**:
  - `python -m ruff check src/backend/`
  - `python -m py_compile src/backend/...`
  - `pytest src/backend/tests -v`
- **Lệnh cấm**: Cấm chạy `pip install` trần trong sandbox; cấm sửa file ngoài `src/backend/`; cấm gọi `pytest`/`ruff` trần của hệ thống không qua môi trường ảo.

---

## 2. Cấu Trúc Thư Mục Chuẩn (`src/backend/`)

```text
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # Khởi tạo FastAPI app, CORS, Lifespan, Exception Handlers
│   ├── core/                 # Cấu hình (config.py), bảo mật (security.py), lỗi chuẩn
│   ├── schemas/              # Pydantic v2 Schemas (Create, Update, Response)
│   ├── services/             # Business Logic & Transaction Management
│   └── api/
│       └── v1/
│           ├── router.py     # Gộp các APIRouter
│           ├── health.py     # Healthcheck endpoint
│           └── users.py      # Resource endpoints (hoặc theo feature)
└── tests/                    # Bộ kiểm thử pytest + httpx.AsyncClient
    ├── conftest.py           # Test fixtures + SQLite async in-memory fallback
    └── test_api_*.py
```

---

## 3. Quy Chuẩn Đồng Bộ Hợp Đồng (Contract Synchronization)

1. **Thống nhất Casing `snake_case`**:
   - Mọi thuộc tính của Pydantic schema và JSON response của REST API thống nhất sử dụng chuẩn **`snake_case`**. Tên trường phải khớp 100% với mục Cross-Layer Data Contract Matrix trong `docs/specs/<feature-slug>/plan.md`.
2. **Pydantic v2 Schema Mẫu**:
   ```python
   from datetime import datetime
   from uuid import UUID
   from pydantic import BaseModel, ConfigDict, Field


   class ItemCreate(BaseModel):
       title: str = Field(..., min_length=1, max_length=255, description="Tiêu đề tài nguyên")
       description: str | None = Field(default=None, max_length=2000, description="Mô tả chi tiết")
       tags: list[str] = Field(default_factory=list, description="Danh sách nhãn")


   class ItemUpdate(BaseModel):
       title: str | None = Field(default=None, min_length=1, max_length=255)
       description: str | None = Field(default=None, max_length=2000)
       tags: list[str] | None = None


   class ItemResponse(BaseModel):
       model_config = ConfigDict(from_attributes=True)

       id: UUID
       title: str
       description: str | None
       tags: list[str]
       created_at: datetime
       updated_at: datetime
   ```
3. **Chuẩn hóa Phản hồi Lỗi (Standard Error Handling)**:
   - Sử dụng `HTTPException(status_code=..., detail="Mô tả lỗi")` nhất quán với API Contract.
   - Không để lộ thông tin nhạy cảm hoặc exception traceback nội bộ ra ngoài client.

---

## 4. Kết Nối Database & Dependency Injection
- Dự án cấu hình `pythonpath = ["src"]` trong `pyproject.toml`, do đó import trực tiếp từ `db`:
  ```python
  from typing import Annotated
  from fastapi import Depends, HTTPException, status
  from sqlalchemy.ext.asyncio import AsyncSession

  from db.models.item import Item
  from db.session import get_db_session
  from db.repositories.item_repository import ItemRepository
  ```
- Sử dụng `Annotated[AsyncSession, Depends(get_db_session)]` cho DI gọn gàng, rõ kiểu:
  ```python
  @router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
  async def create_item(
      payload: ItemCreate,
      session: Annotated[AsyncSession, Depends(get_db_session)],
  ):
      service = ItemService(session)
      return await service.create(payload)
  ```
- Endpoint POST trả về `status_code=status.HTTP_201_CREATED`, DELETE trả về `status_code=status.HTTP_204_NO_CONTENT`.

---

## 5. Tham Gia Vòng Lặp Sửa Lỗi (Feedback Loop Protocol)
Khi nhận tin nhắn `[SELF-HEALING ACTION REQUIRED]` từ QA hoặc `[REVIEW-FIX ACTION REQUIRED]` từ Reviewer:
1. Xác định lỗi từ file, dòng code và traceback được cung cấp qua `scripts/parse_traceback.py`.
2. Sửa lỗi trong `src/backend/`, chạy smoke test: `python -m ruff check src/backend/` và `pytest src/backend/tests`.
3. Phản hồi cho Tech Lead bằng thông điệp `[FIX-COMPLETED]`.
