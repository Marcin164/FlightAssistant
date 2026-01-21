from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
import os
import httpx

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # In production you should fail fast or ensure env is configured via secrets manager
    OPENAI_API_KEY = ""

class Message(BaseModel):
    role: str = Field(..., regex="^(user|system|assistant)$")
    content: str

class ChatRequest(BaseModel):
    model: Optional[str] = "gpt-3.5-turbo"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    raw: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_proxy(payload: ChatRequest):
    """Proxy endpoint to OpenAI Chat Completions (non-streaming)."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": payload.model,
        "messages": [
            {"role": m.role, "content": m.content} for m in payload.messages
        ],
        "temperature": payload.temperature,
        "max_tokens": payload.max_tokens,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, json=body, headers=headers)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting OpenAI: {e}")

    if resp.status_code != 200:
        # bubble up a useful error message
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=502, detail={"openai_error": detail})

    data = resp.json()
    # Extract the assistant reply (first choice)
    try:
        reply = data["choices"][0]["message"]["content"]
    except Exception:
        reply = ""

    return ChatResponse(reply=reply, raw=data)

