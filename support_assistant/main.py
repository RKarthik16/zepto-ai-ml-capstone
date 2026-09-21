from fastapi import FastAPI, HTTPException

from support_assistant.graph import SupportAssistant
from support_assistant.schemas import AskRequest, AskResponse
from support_assistant.config import MOCK_LLM

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline policy-based customer support assistant",
    version="1.0.0",
)

assistant = SupportAssistant()


@app.get("/")
def root():
    return {
        "service": "Zepto Support Assistant",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "mock_llm": MOCK_LLM,
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        return assistant.ask(request.query)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to process the question: {exc}",
        ) from exc