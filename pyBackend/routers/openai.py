from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
import os
import httpx
import json

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # In production you should fail fast or ensure env is configured via secrets manager
    OPENAI_API_KEY = ""

class Message(BaseModel):
    role: str = Field(..., regex="^(user|system|assistant)$")
    content: str

class ChatRequest(BaseModel):
    model: Optional[str] = "gpt-4o-mini"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    raw: Optional[Dict[str, Any]] = None

class FlightDetailsRequest(BaseModel):
    flight_number: str = Field(..., description="Flight number (e.g., 'LO123', 'FR4567')")

class FlightDetailsResponse(BaseModel):
    flightNumber: str
    airline: str
    flight_from: str = Field(..., alias="from")
    flight_to: str = Field(..., alias="to")
    departureTime: str
    arrivalTime: str
    gate: str
    terminal: str
    status: str
    delayMinutes: Optional[int] = None

    class Config:
        populate_by_name = True

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


@router.options("/flight-details")
async def flight_details_options():
    """Handle CORS preflight requests for flight-details endpoint."""
    return {}

@router.post("/flight-details", response_model=Dict[str, Any])
async def get_flight_details(payload: FlightDetailsRequest):
    """Get flight details using OpenAI API based on flight number."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    system_prompt = """
Jesteś systemem informacji lotniskowej.

Użytkownik podaje numer lotu (np. "LO123", "FR4567").
Twoim zadaniem jest zwrócić szczegółowe informacje o locie.

ZASADY:
- Jeśli numer lotu wygląda poprawnie, ZAWSZE zwróć dane
- Dane mogą być symulowane, ale muszą być realistyczne
- Odpowiadaj WYŁĄCZNIE w formacie JSON
- Nie dodawaj żadnego tekstu poza JSON

FORMAT JSON:
{
  "flightNumber": string,
  "airline": string,
  "from": string,
  "to": string,
  "departureTime": string,
  "arrivalTime": string,
  "gate": string,
  "terminal": string,
  "status": "On Time" | "Delayed" | "Boarding" | "Cancelled",
  "delayMinutes": number | null
}
"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload.flight_number},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, json=body, headers=headers)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting OpenAI: {e}")

    if resp.status_code != 200:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=502, detail={"openai_error": detail})

    data = resp.json()

    # Extract the assistant reply (first choice)
    try:
        reply = data["choices"][0]["message"]["content"]
        flight_data = json.loads(reply)
        return flight_data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"Failed to parse flight data from AI response: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error processing flight details: {e}")


@router.get("/flight-details", response_model=Dict[str, Any])
async def get_flight_details_query(flight_number: str = Query(..., description="Flight number (e.g., 'LO123', 'FR4567')")):
    """Get flight details using OpenAI API - GET variant with query parameter."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    system_prompt = """
Jesteś systemem informacji lotniskowej.

Użytkownik podaje numer lotu (np. "LO123", "FR4567").
Twoim zadaniem jest zwrócić szczegółowe informacje o locie.

ZASADY:
- Jeśli numer lotu wygląda poprawnie, ZAWSZE zwróć dane
- Dane mogą być symulowane, ale muszą być realistyczne
- Odpowiadaj WYŁĄCZNIE w formacie JSON
- Nie dodawaj żadnego tekstu poza JSON

FORMAT JSON:
{
  "flightNumber": string,
  "airline": string,
  "from": string,
  "to": string,
  "departureTime": string,
  "arrivalTime": string,
  "gate": string,
  "terminal": string,
  "status": "On Time" | "Delayed" | "Boarding" | "Cancelled",
  "delayMinutes": number | null
}
"""

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": flight_number},
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, json=body, headers=headers)
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Error contacting OpenAI: {e}")

    if resp.status_code != 200:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise HTTPException(status_code=502, detail={"openai_error": detail})

    data = resp.json()

    # Extract the assistant reply (first choice)
    try:
        reply = data["choices"][0]["message"]["content"]
        flight_data = json.loads(reply)
        return flight_data
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"Failed to parse flight data from AI response: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error processing flight details: {e}")


