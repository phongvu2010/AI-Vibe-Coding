"""Pydantic Schemas for Structured SDLC Artifacts in AI-Vibe-Coding (`scripts/schemas.py`).
Enables machine-validated data contracts across all 5 Sub-Teams and Quality Gates.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# =============================================================================
# GATE & STATE SCHEMAS
# =============================================================================

class GateDecisionStatus(str, Enum):
    APPROVED = "APPROVED"
    REVISION_REQUESTED = "REVISION_REQUESTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"


class GateDecision(BaseModel):
    gate_id: str = Field(description="Mã Gate (vd: gate_1_client_signoff)")
    reviewer: str = Field(default="Tech Lead / Product Owner", description="Tên hoặc vai trò người ký duyệt")
    status: GateDecisionStatus = Field(default=GateDecisionStatus.APPROVED, description="Quyết định ký duyệt")
    feedback: str = Field(default="", description="Ý kiến chỉ đạo hoặc yêu cầu sửa đổi")
    timestamp: Optional[str] = Field(default=None, description="Thời gian ký duyệt")


# =============================================================================
# SUB-TEAM 1: PRODUCT DISCOVERY SCHEMAS
# =============================================================================

class ClarificationQnAModel(BaseModel):
    q_id: str = Field(description="Mã câu hỏi (vd: Q-01)")
    context: str = Field(description="Điểm chưa rõ hoặc giả định trong yêu cầu gốc")
    impact: str = Field(description="Tác động kỹ thuật hoặc nghiệp vụ nếu không làm rõ")
    proposed_solution: str = Field(description="Đề xuất gợi ý cho khách hàng lựa chọn")


class UserStoryModel(BaseModel):
    id: str = Field(description="Mã Story (vd: US-01)")
    epic: str = Field(default="Core", description="Tên Epic hoặc phân hệ")
    title: str = Field(description="Tiêu đề User Story")
    as_a: str = Field(description="Vai trò người dùng (As a...)")
    i_want_to: str = Field(description="Hành động mong muốn (I want to...)")
    so_that: str = Field(description="Mục đích / Giá trị (So that...)")
    priority: str = Field(default="MUST_HAVE", description="Độ ưu tiên: MUST_HAVE, SHOULD_HAVE, COULD_HAVE")
    story_points: int = Field(default=3, description="Ước lượng độ phức tạp (1, 2, 3, 5, 8)")
    acceptance_criteria_gherkin: str = Field(
        description="Tiêu chí nghiệm thu chuẩn cú pháp Gherkin (Scenario, Given, When, Then)"
    )


class FunctionalRequirementModel(BaseModel):
    code: str = Field(description="Mã yêu cầu (vd: FR-01)")
    name: str = Field(description="Tên tính năng chức năng")
    description: str = Field(description="Mô tả tóm tắt tính năng")
    priority: str = Field(default="P0 (Must Have)", description="Độ ưu tiên: P0, P1, P2")
    subteam: str = Field(default="Core Engineering", description="Đội ngũ phụ trách")


class BusinessRuleModel(BaseModel):
    rule_id: str = Field(description="Mã quy tắc nghiệp vụ (vd: BR-01)")
    name: str = Field(description="Tên quy tắc")
    statement: str = Field(description="Nội dung ràng buộc nghiệp vụ")
    enforcement_layer: str = Field(default="Service", description="Tầng xử lý: Service, DB, Router")


class DiscoveryResult(BaseModel):
    """Kết quả hoàn chỉnh từ Sub-Team 1 (Product Discovery & Solutions)."""
    project_name: str = Field(description="Tên dự án chuẩn hóa")
    project_vision: str = Field(description="Tầm nhìn sản phẩm và mục tiêu cốt lõi")
    business_goals: List[str] = Field(default_factory=list, description="Danh sách mục tiêu kinh doanh định lượng")
    in_scope_mvp: List[str] = Field(default_factory=list, description="Các tính năng nằm trong phạm vi MVP v1.0")
    out_of_scope: List[str] = Field(default_factory=list, description="Các tính năng dành cho phiên bản tương lai")
    clarifications: List[ClarificationQnAModel] = Field(default_factory=list)
    user_stories: List[UserStoryModel] = Field(default_factory=list)
    functional_requirements: List[FunctionalRequirementModel] = Field(default_factory=list)
    business_rules: List[BusinessRuleModel] = Field(default_factory=list)
    ui_ux_screen_flows: List[str] = Field(default_factory=list, description="Danh sách màn hình và luồng điều hướng")


# =============================================================================
# SUB-TEAM 2: ARCHITECTURE & PLANNING SCHEMAS
# =============================================================================

class TechStackSelection(BaseModel):
    backend_framework: str = Field(default="Python (FastAPI v0.110+)")
    backend_orm: str = Field(default="SQLAlchemy 2.0 (Async Declarative)")
    data_validation: str = Field(default="Pydantic v2 (snake_case)")
    frontend_web: str = Field(default="Next.js 15 (App Router) / React Vite")
    frontend_mobile: str = Field(default="React Native Expo (NativeWind v4)")
    database: str = Field(default="PostgreSQL 16+ & SQLite (test)")
    caching_session: str = Field(default="Redis 7.0+ / Local Cache")
    api_specification: str = Field(default="OpenAPI 3.0.3 (Contract-First)")
    rationale: str = Field(default="Clean Architecture, High Performance, Manual Review Friendly")


class ADRModel(BaseModel):
    id: str = Field(description="Mã ADR (vd: ADR-01)")
    title: str = Field(description="Tiêu đề quyết định kiến trúc")
    context: str = Field(description="Bối cảnh kỹ thuật")
    decision: str = Field(description="Quyết định lựa chọn")
    consequences: str = Field(description="Hệ quả và lợi ích mang lại")


class APIEndpointModel(BaseModel):
    path: str = Field(description="Đường dẫn endpoint (vd: /api/v1/orders)")
    method: str = Field(description="Phương thức HTTP: GET, POST, PUT, DELETE")
    summary: str = Field(description="Tóm tắt chức năng")
    tags: List[str] = Field(default_factory=list)
    request_body_schema: Optional[str] = None
    response_schema: str = Field(description="Tên schema trả về")
    status_code: int = Field(default=200)


class DatabaseTableModel(BaseModel):
    table_name: str
    description: str
    columns: List[str]
    relationships: List[str] = Field(default_factory=list)


class ArchitectureResult(BaseModel):
    """Kết quả hoàn chỉnh từ Sub-Team 2 (Architecture & System Planning)."""
    project_name: str
    tech_stack: TechStackSelection = Field(default_factory=TechStackSelection)
    adrs: List[ADRModel] = Field(default_factory=list)
    endpoints: List[APIEndpointModel] = Field(default_factory=list)
    database_tables: List[DatabaseTableModel] = Field(default_factory=list)
    openapi_yaml: str = Field(default="", description="Nội dung đặc tả OpenAPI 3.0.3")
    erd_mermaid: str = Field(default="", description="Sơ đồ quan hệ ERD cú pháp Mermaid")
    security_stride_matrix: List[Dict[str, str]] = Field(default_factory=list)
    tasks_backlog: List[Dict[str, Any]] = Field(default_factory=list, description="Danh sách Task DAG có depends_on")


# =============================================================================
# SUB-TEAM 4: QUALITY, SECURITY & AUTO-HEALING SCHEMAS
# =============================================================================

class DefectTicket(BaseModel):
    """Phiếu ghi nhận lỗi phục vụ vòng lặp tự sửa lỗi (Auto-Healing)."""
    id: str = Field(description="Mã lỗi (vd: DEF-01)")
    target_team: str = Field(default="backend", description="Phân đội phụ trách: backend, frontend, db, devops")
    file_path: str = Field(description="Đường dẫn file bị lỗi")
    severity: str = Field(default="HIGH", description="Mức độ nghiêm trọng: CRITICAL, HIGH, MEDIUM, LOW")
    issue_description: str = Field(description="Mô tả lỗi hoặc lý do test thất bại")
    suggested_fix: str = Field(default="", description="Gợi ý phương án sửa chữa")
    resolved: bool = Field(default=False, description="Trạng thái đã được giải quyết chưa")
    stack_trace: Optional[str] = Field(default=None, description="Trích đoạn stack trace liên quan")
    patch_summary: Optional[str] = Field(default=None, description="Tóm tắt bản vá đã áp dụng")


class QAEvaluationResult(BaseModel):
    passed: bool
    coverage_score: float = Field(default=0.0, description="Độ phủ code kiểm thử (%)")
    total_defects: int = Field(default=0)
    defects: List[DefectTicket] = Field(default_factory=list)
    summary: str = Field(default="")


class CodeReviewMetric(BaseModel):
    category: str = Field(description="Tên hạng mục đánh giá")
    score: float = Field(description="Điểm số (thang 10 hoặc 100)")
    standard: str = Field(description="Tiêu chuẩn so sánh")
    comment: str = Field(description="Nhận xét chi tiết")


class SecurityCheckItem(BaseModel):
    code: str = Field(description="Mã rủi ro (vd: OWASP-API1, OWASP-API2)")
    name: str = Field(description="Tên lỗ hổng OWASP")
    status: str = Field(default="PASSED", description="PASSED hoặc FAILED")
    details: str = Field(default="", description="Chi tiết kiểm tra")


class QAReportResult(BaseModel):
    """Kết quả tổng hợp từ Sub-Team 4 (QA & Security Audit)."""
    clean_architecture_score: float = 9.5
    typing_score: float = 10.0
    security_score: float = 9.8
    overall_score: float = 9.8
    scorecard: List[CodeReviewMetric] = Field(default_factory=list)
    secret_leaks_found: List[str] = Field(default_factory=list)
    owasp_checks: List[SecurityCheckItem] = Field(default_factory=list)
    test_metrics: Dict[str, Any] = Field(default_factory=dict)
