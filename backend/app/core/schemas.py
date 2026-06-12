from pydantic import BaseModel
from typing import Any, Optional

class AuditRecord(BaseModel):
    area: str
    owner: str
    impact: int = 3
    likelihood: int = 3
    openFindings: int = 0
    repeatIssues: int = 0
    controlMaturity: int = 3
    overdueDays: int = 0
    regulatoryChange: int = 0
    materiality: int = 3
    branchType: str = "Retail"
    productLine: str = "Deposits"
    note: str = ""

class RiskItem(BaseModel):
    area: str
    owner: str
    branchType: str
    productLine: str
    score: int
    level: str
    drivers: list[str]
    recommendation: str
    note: str

class RiskResponse(BaseModel):
    items: list[dict[str, Any]]

class ChatRequest(BaseModel):
    question: str

class GuardrailsInfo(BaseModel):
    allowed: bool
    in_scope: bool
    human_review_required: bool
    negative_test: dict[str, Any]
    pii_redaction: dict[str, Any]
    safe_question: str

class ChatResponse(BaseModel):
    answer: str
    context: list[dict[str, Any]]
    type: str = "normal"
    in_scope: bool = True
    guardrails: Optional[GuardrailsInfo] = None