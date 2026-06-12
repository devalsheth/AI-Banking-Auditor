from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.services.bootstrap import bootstrap_knowledge_base

app = FastAPI(title="Banking Audit Risk Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event() -> None:
    bootstrap_knowledge_base()

app.include_router(router, prefix="/api")

@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "banking-audit-risk-assistant"}
