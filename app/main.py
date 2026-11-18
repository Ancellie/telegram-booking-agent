from fastapi import FastAPI, HTTPException
from app.schemas.requests import ResolveContextRequest, BuildPromptRequest, ParseReplyRequest
from app.services.agent import resolve_context, build_clock, build_prompt, parse_reply

app = FastAPI(title="Sky Restaurant Booking Agent API", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True, "service": "sky-restaurant-agent"}

@app.post("/api/resolve-context")
def resolve(payload: ResolveContextRequest):
    result = resolve_context(payload.items)
    if result is None:
        return {"skip": True, "context": None}
    return {"skip": False, "context": build_clock(result)}

@app.post("/api/build-prompt")
def prompt(payload: BuildPromptRequest):
    try:
        return build_prompt(payload.context)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not build prompt: {exc}")

@app.post("/api/parse-reply")
def parse(payload: ParseReplyRequest):
    try:
        return parse_reply(payload.context, payload.parsed, payload.llm_error)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not parse LLM reply: {exc}")
