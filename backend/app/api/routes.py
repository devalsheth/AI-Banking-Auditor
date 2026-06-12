from fastapi import APIRouter, UploadFile, File
from app.core.schemas import AuditRecord, RiskResponse, ChatRequest, ChatResponse
from app.services.synthetic_data import generate_synthetic_audits
from app.services.risk_engine import score_records
from app.services.vector_store import search_context
from app.services.agent_service import generate_explanation
from app.core.guardrails import guard_question
import csv
import io
import random

router = APIRouter()

ALLOWED_KEYWORDS = [
    "audit", "bank", "banking", "risk", "finding", "findings",
    "regulation", "regulatory", "compliance", "kyc", "aml",
    "csv", "dashboard", "control", "controls", "priority",
    "prioritization", "remediation", "policy", "circular", "npa"
]

DEFAULT_FALLBACKS = [
    "I’m specialized in banking audit intelligence and this demo supports audit findings, risk prioritization, regulatory updates, uploaded CSV data, and audit workflow questions. Please ask something related to the audit dashboard or banking audit process.",
    "That looks outside my current scope. I can help with banking audit data, findings analysis, regulatory impact, risk scoring, and dashboard insights.",
    "I may not provide a reliable answer for that topic. Please ask about audit findings, compliance, regulatory updates, CSV uploads, or risk prioritization."
]

def is_in_scope(question: str) -> bool:
    text = (question or "").lower()
    return any(keyword in text for keyword in ALLOWED_KEYWORDS)

def get_fallback_reply() -> str:
    return random.choice(DEFAULT_FALLBACKS)

@router.get("/synthetic-data")
def get_synthetic_data(count: int = 20):
    records = generate_synthetic_audits(count)
    scored = score_records(records)
    return {"items": scored}

@router.post("/score", response_model=RiskResponse)
def score_payload(records: list[AuditRecord]):
    scored = score_records([record.model_dump() for record in records])
    return {"items": scored}

@router.post("/upload-csv", response_model=RiskResponse)
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    rows = [dict(row) for row in reader]
    scored = score_records(rows)
    return {"items": scored}

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    guard = guard_question(req.question)

    if not guard["allowed"]:
        return {
            "answer": "Blocked by security guardrails. Please remove sensitive data and keep the request within banking audit scope.",
            "context": [],
            "type": "blocked",
            "in_scope": guard["in_scope"],
            "guardrails": guard,
        }

    if not is_in_scope(req.question):
        return {
            "answer": get_fallback_reply(),
            "context": [],
            "type": "fallback",
            "in_scope": False,
            "guardrails": guard,
        }

    context = search_context(guard["safe_question"], top_k=5)

    if not context:
        return {
            "answer": "I couldn’t find enough relevant banking audit context to answer reliably. Please ask about audit findings, risk scoring, regulatory updates, CSV data, or audit workflow.",
            "context": [],
            "type": "fallback",
            "in_scope": False,
            "guardrails": guard,
        }

    answer = generate_explanation(guard["safe_question"], context)
    return {
        "answer": answer,
        "context": context,
        "type": "normal",
        "in_scope": True,
        "guardrails": guard,
    }