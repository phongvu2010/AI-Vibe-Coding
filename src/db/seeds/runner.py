import asyncio

from src.db.models.user import User
from src.db.repositories.user_repository import UserRepository
from src.db.session import AsyncSessionLocal


async def seed_data():
    """Khởi tạo dữ liệu mẫu ban đầu"""
    print("🌱 [SEED RUNNER] Đang khởi tạo dữ liệu mẫu cho hệ thống...")
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        existing = await repo.get_by_email("admin@vibe.dev")
        if not existing:
            admin_user = User(
                email="admin@vibe.dev",
                full_name="Tech Lead Administrator",
                is_active=True
            )
            await repo.create(admin_user)
            await session.commit()
            print(f"✅ Đã tạo tài khoản mẫu: {admin_user.email} ({admin_user.id})")
        else:
            print(f"ℹ️ Tài khoản mẫu {existing.email} đã tồn tại.")

if __name__ == "__main__":
    asyncio.run(seed_data())
