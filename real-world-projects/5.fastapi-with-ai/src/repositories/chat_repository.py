
from src.schemas.chat_schema import ChatRequest
from src.core.helpers import get_ai_platform


def chat(data: ChatRequest):
    platform = get_ai_platform(data.model_name)
    response_text = platform.chat(data.prompt)
    return response_text