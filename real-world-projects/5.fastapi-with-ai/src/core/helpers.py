from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import select, Session

from src.models.user import User
from src.ai.gemini import Gemini
from src.core.config import settings
from src.core.enums import AIModels


PLATFORM_MAP = {
    AIModels.GEMINI: Gemini
}


def check_email_exists(email: str, db: Session, user: Optional[User] = None):
    query = select(User).where(User.email == email)
    if user:
        query = query.where(User.id != user.id)

    return db.scalar(query)


def check_username_exists(username: str, db: Session, user: Optional[User] = None):
    query = select(User).where(User.username == username)
    if user:
        query = query.where(User.id != user.id)

    return db.scalar(query)


def load_system_prompt():
    try:
        with open('src/prompts/system-prompt.md') as f:
            return f.read()
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f'Missing system prompt file: {str(e)}'
        )
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f'Error loading prompt: {str(e)}'
        )

    

def get_ai_platform(model_name: AIModels):
    system_prompt = load_system_prompt()

    platform_class = PLATFORM_MAP.get(model_name)

    if not platform_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"AI platform '{model_name.value.upper()}' not found."
        )

    api_key_setting_name = f"{model_name.value.upper()}_API_KEY"
    api_key = getattr(settings, api_key_setting_name, None)
    if not api_key:
        raise ValueError(f"API KEY environment variable for {model_name} not set.")
    
    return platform_class(api_key=api_key, system_prompt=system_prompt)