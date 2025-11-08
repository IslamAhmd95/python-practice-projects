from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from src.ai.gemini import Gemini
from src.core.config import settings


# Initialize application
app = FastAPI(
    title="FastAPI Gemini Ai App"
)



# Ai Configuration
def load_system_prompt():
    try:
        with open('src/prompts/system-prompt.md') as f:
            return f.read()
    except Exception as e:
        raise Exception(f'Error: {str(e)}')

system_prompt = load_system_prompt()
gemini_api_key = settings.GEMINI_API_KEY

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


# Pydantic Models
class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


# API Endpoints
@app.post('/chat', response_model=ChatResponse)
def char(request: ChatRequest):
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)
