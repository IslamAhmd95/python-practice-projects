from fastapi import APIRouter, Depends

from src.schemas.chat_schema import ChatRequest, ChatResponse
from src.core.oauth2 import get_current_user
from src.repositories import chat_repository



router = APIRouter(
    prefix="/chat", tags=["Chat"]
)


@router.post('/', dependencies=[Depends(get_current_user)], response_model=ChatResponse)
def char(data: ChatRequest):
    response_text = chat_repository.chat(data)
    return ChatResponse(response=response_text)
