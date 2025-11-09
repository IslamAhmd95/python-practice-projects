from pydantic import BaseModel
from src.core.enums import AIModels


class ChatRequest(BaseModel):
    model_name: AIModels = AIModels.GEMINI
    prompt: str


class ChatResponse(BaseModel):
    response: str