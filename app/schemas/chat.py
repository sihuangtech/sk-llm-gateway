from pydantic import BaseModel

class ChatRequest(BaseModel):
    model: str | None = None
    messages: list
    stream: bool = False

class ChatResponse(BaseModel):
    content: str
