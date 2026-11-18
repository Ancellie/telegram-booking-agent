from typing import Any
from pydantic import BaseModel, Field

class ResolveContextRequest(BaseModel):
    items: list[dict[str, Any]] = Field(default_factory=list)

class BuildPromptRequest(BaseModel):
    context: dict[str, Any]

class ParseReplyRequest(BaseModel):
    context: dict[str, Any]
    parsed: dict[str, Any] | None = None
    llm_error: str = ""
