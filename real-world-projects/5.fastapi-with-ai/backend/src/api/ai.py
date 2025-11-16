from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.models.user import User
from src.core.oauth2 import get_current_user
from src.repositories import ai_repository
from src.core.enums import AIModels
from src.core.database import get_db
from src.schemas.ai_schema import (
    ChatRequest, ChatResponse, GetPlatforms, Chat, ChatHistoryResponse
)


router = APIRouter(
    prefix="/ai", tags=["Ai"]
)


@router.post('/chat', response_model=ChatResponse)
def chat(data: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    response_text = ai_repository.chat(data, current_user, db)
    return ChatResponse(response=response_text)


@router.get('/platforms', response_model=GetPlatforms)
def get_platforms():
    return {"platforms": list(AIModels)}


@router.get('/chat-history', response_model=ChatHistoryResponse)
def get_chat_history(model_name: AIModels, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_records = ai_repository.get_chat_history(model_name, current_user, db)
    return ChatHistoryResponse(chat=chat_records)