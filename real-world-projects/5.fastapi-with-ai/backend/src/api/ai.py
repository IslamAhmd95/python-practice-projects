from fastapi import APIRouter, Depends

from src.core.oauth2 import get_current_user
from src.repositories import ai_repository
from src.core.enums import AIModels
from src.schemas.ai_schema import (
    ChatRequest, ChatResponse, GetPlatforms
)



router = APIRouter(
    prefix="/ai", tags=["Ai"]
)


@router.post('/chat', dependencies=[Depends(get_current_user)], response_model=ChatResponse)
def chat(data: ChatRequest):
    response_text = ai_repository.chat(data)
    return ChatResponse(response=response_text)


@router.get('/platforms', response_model=GetPlatforms)
def get_platforms():
    return {"platforms": list(AIModels)}