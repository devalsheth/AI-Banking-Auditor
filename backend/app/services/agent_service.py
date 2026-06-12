from app.core.config import settings
import httpx

SYSTEM_PROMPT = """You are an audit risk assessment assistant for banking and financial institutions.
Use the retrieved context to answer in concise business language.
Explain why the audit area is risky, what evidence matters, and what should be prioritized next.
If API access is unavailable, still provide a grounded answer from retrieved context.
If the user asks something outside banking audit, compliance, controls, findings, remediation, risk scoring, regulatory updates, or uploaded audit data, do not answer the unrelated topic. Instead say the request is outside scope and guide the user back to supported topics."""

def generate_explanation(question: str, context: list[dict]) -> str:
    context_text = "\n".join([f"- [{c.get('source','ctx')}] {c.get('text','')}" for c in context])
    if not settings.tcs_api_key:
        return f"Context-based answer:{context_text}Recommended response: Focus the audit on areas with high unresolved findings, weak controls, overdue remediation, and regulatory sensitivity."

    payload = {
        "model": settings.tcs_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {question}Context:{context_text}"}
        ],
        "temperature": 0.2
    }

    headers = {
        "Authorization": f"Bearer {settings.tcs_api_key}",
        "Content-Type": "application/json"
    }

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                f"{settings.tcs_base_url}/openai/v1/chat/completions",
                json=payload,
                headers=headers
            )
            resp.raise_for_status()
            data = resp.json()
            return data['choices'][0]['message']['content']
    except Exception:
        return f"Context-based answer:{context_text}Recommended response: Prioritize high-risk banking processes first and validate remediation evidence before scoping fieldwork."