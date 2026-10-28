# 🚀 WORKSPACE OUTPUT PROJECT (RUNTIME DIRECTORY)

Thư mục này là **Runtime Output Workspace** dành cho các tác tử AI (Sub-Team 3 & Sub-Team 4).

Khi bạn khởi chạy chu trình SDLC bằng lệnh:
```bash
make dev PROJECT="Tên_Dự_Án" FILE="workspaces/sample_client_brief.md" PLATFORM="web"
```
Mã nguồn hoàn chỉnh của dự án mới (Backend FastAPI, Frontend React/React Native, và Docker Compose) sẽ được tự động sinh và kiểm thử trực tiếp tại đây:
- `backend/`: FastAPI application, SQLAlchemy 2.0 models, Alembic migrations, PyTest suite.
- `frontend/`: Web application (Next.js 15 / React Vite) hoặc Mobile App (React Native Expo).
- `infra/`: Dockerfile, docker-compose.yml, cấu hình môi trường.

---

> 💡 **Gợi ý:** Để xem mã nguồn dự án mẫu hoàn chỉnh đã được kiểm thử đạt $\ge 90\%$ Code Coverage & Zero Schema Drift, hãy tham khảo thư mục: [`examples/motocare_reference/output_project/`](../../examples/motocare_reference/output_project/).
