# Banking Audit Risk Assessment Assistant

Full-stack starter project for a banking and financial institution audit assistant using:
- Angular frontend
- Python FastAPI backend
- FAISS vector database
- Synthetic audit data generation
- TCS-hosted LLM integration hooks

## Architecture
- `frontend/` Angular dashboard UI
- `backend/` FastAPI app with scoring, synthetic data, retrieval, and agent orchestration
- `docs/` setup and demo notes

## Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Frontend setup
```bash
cd frontend
npm install
npm start
```

## Notes
- Put your TCS credentials in `backend/.env`.
- The FAISS index is built from synthetic findings and regulatory context at startup.
- This is a hackathon-ready starter with domain-specific banking audit modules.
