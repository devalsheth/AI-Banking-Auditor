import re
from typing import Any

PII_PATTERNS = {
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone": r"\b(?:\+?\d{1,3}[-. ]?)?(?:\d{10}|(?:\d{3}[-. ]\d{3}[-. ]\d{4}))\b",
    "credit_card": r"\b(?:\d[ -]*?){13,19}\b",
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "account": r"\b\d{9,18}\b",
}

def redact_pii(text: str) -> dict[str, Any]:
    findings = []
    redacted = text or ""
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, redacted)
        if matches:
            findings.extend([{"type": label, "value": m} for m in matches])
            redacted = re.sub(pattern, f"[{label.upper()}_REDACTED]", redacted)
    return {"redacted": redacted, "findings": findings}

def negative_test(text: str) -> dict[str, Any]:
    issues = []
    if not (text or "").strip():
        issues.append("empty_input")
    if len(text or "") > 4000:
        issues.append("too_long")
    if re.search(r"ignore\s+previous|reveal\s+system|bypass\s+policy|show\s+secrets", text or "", re.I):
        issues.append("prompt_injection")
    return {"passed": len(issues) == 0, "issues": issues}

def scope_check(question: str) -> dict[str, Any]:
    q = (question or "").lower()
    in_scope = any(k in q for k in ["bank", "banking", "audit", "risk", "controls", "compliance", "npa"])
    return {"in_scope": in_scope}

def guard_question(question: str) -> dict[str, Any]:
    red = redact_pii(question)
    neg = negative_test(question)
    scope = scope_check(question)
    allowed = neg["passed"] and scope["in_scope"]
    return {
        "allowed": allowed,
        "in_scope": scope["in_scope"],
        "negative_test": neg,
        "pii_redaction": red,
        "human_review_required": bool(red["findings"]) or not scope["in_scope"] or not neg["passed"],
        "safe_question": red["redacted"],
    }