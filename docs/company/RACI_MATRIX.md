# Ma Trận Phân Công Trách Nhiệm RACI (RACI Matrix)
### AI-Vibe-Coding Software House

Ma trận RACI định nghĩa rõ vai trò của từng Tác tử trong 7 Giai đoạn phát triển:
- **R (Responsible)**: Tác tử trực tiếp thực hiện công việc.
- **A (Accountable)**: Tác tử chịu trách nhiệm nghiệm thu và kết quả cuối cùng (Tech Lead / Client).
- **C (Consulted)**: Tác tử được tham vấn chuyên môn (2 chiều).
- **I (Informed)**: Tác tử được thông báo kết quả (1 chiều).

---

## 📊 Bảng Ma Trận RACI 7 Giai Đoạn

| Giai đoạn SDLC | User (PO) | Tech Lead | Sub-Team 1 (Discovery) | Sub-Team 2 (Architecture) | Sub-Team 3 (Dev Squad) | Sub-Team 4 (QA & Review) | Sub-Team 5 (Release) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0. Discovery & PRD** | **A** | C | **R** (`lead-ba`, `account-lead`) | I | I | I | I |
| **Gate 1: Client Sign-off** | **A** | C | **R** | I | I | I | I |
| **1. Architecture & Contracts**| I | **A** | C | **R** (`system`, `security`, `planner`) | C | C | I |
| **Gate 2: Technical Sign-off** | I | **A** | I | **R** | C | I | I |
| **2. Guardrails Setup** | I | **R / A** | I | I | C | I | I |
| **3. 2-Wave Core Engineering** | I | **A** | I | C | **R** (`db`, `backend`, `frontend`) | I | I |
| **Handshake Gate** | I | **A** | I | I | **R** | I | I |
| **4. Automated QA Testing** | I | **A** | I | I | C (Self-Healing) | **R** (`qa-tester`) | I |
| **5. Principal Code Review** | I | **A** | I | I | C (Review-Fix) | **R** (`code-reviewer`) | I |
| **Gate 3: Production Sign-off**| I | **A** | I | I | I | **R** | I |
| **6. Release & Handover** | **A** | C | I | I | I | I | **R** (`release`, `writer`, `handover`) |

---

## 🎯 Nguyên Tắc Phối Hợp
1. **Một việc một chủ thể chịu trách nhiệm (Single Accountability)**: Luôn chỉ có 1 tác tử giữ vai trò **A** tại mỗi Quality Gate.
2. **Khách hàng chỉ tham gia tại các chốt chặn then chốt**: Khách hàng (User) giữ vai trò **A** tại Gate 1 (Scope & PRD) và Gate 6 (Nghiệm thu UAT cuối cùng). Toàn bộ các khâu kỹ thuật trung gian do Tech Lead và Reviewer bảo đảm.
