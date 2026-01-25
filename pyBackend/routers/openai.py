import httpx
import json
import numpy as np
import os
import pandas as pd
import pickle
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from pydantic import BaseModel, Field
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional, Any, Dict

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # In production you should fail fast or ensure env is configured via secrets manager
    OPENAI_API_KEY = ""

# Vector Database Configuration
VECTORS_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "vectors_db")
_vectorizer = None
_vectors = None
_metadata = None
_documents = None


def _load_vector_db():
    """Load vector database (vectors, vectorizer, and metadata)."""
    global _vectorizer, _vectors, _metadata

    if _vectors is not None:
        return  # Already loaded

    try:
        vectors_dir = Path(VECTORS_DB_DIR)

        if not vectors_dir.exists():
            print(f"⚠️ Vector database directory not found: {VECTORS_DB_DIR}")
            return

        # Load vectors
        with open(vectors_dir / 'vectors.pkl', 'rb') as f:
            _vectors = pickle.load(f)

        # Load vectorizer
        with open(vectors_dir / 'vectorizer.pkl', 'rb') as f:
            _vectorizer = pickle.load(f)

        # Load metadata
        _metadata = pd.read_csv(vectors_dir / 'metadata.csv').to_dict('records')

        print(f"✅ Vector database loaded successfully")
    except Exception as e:
        print(f"❌ Error loading vector database: {e}")


def _search_vectors(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search similar documents in vector database.

    Args:
        query: Search query text
        top_k: Number of results to return

    Returns:
        List of similar documents with scores
    """
    global _vectorizer, _vectors, _metadata

    if _vectorizer is None or _vectors is None:
        _load_vector_db()

    if _vectorizer is None or _vectors is None:
        return []

    try:
        # Transform query to vector
        query_vector = _vectorizer.transform([query])

        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, _vectors)[0]

        # Get top k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # Create results
        results = []
        for idx in top_indices:
            results.append({
                'filename': _metadata[idx]['filename'],
                'similarity_score': float(similarities[idx]),
                'index': int(idx)
            })

        return results
    except Exception as e:
        print(f"❌ Error searching vectors: {e}")
        return []


def _get_document_content(doc_index: int) -> Optional[str]:
    """
    Get document content by index (loads from file).

    Args:
        doc_index: Document index

    Returns:
        Document content as string
    """
    if _metadata is None or doc_index >= len(_metadata):
        return None

    try:
        doc_path = _metadata[doc_index]['path']
        with open(doc_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading document: {e}")
        return None


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
    """Proxy endpoint to OpenAI Chat Completions with vector database context."""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    # Prepare context from vector database
    context = ""
    user_message_text = payload.messages[-1].content if payload.messages else ""

    if user_message_text:
        # Search for relevant documents
        search_results = _search_vectors(user_message_text, top_k=5)

        if search_results:
            context = "\n=== RELEVANT KNOWLEDGE BASE DOCUMENTS ===\n"
            for result in search_results:
                context += f"\nDocument: {result['filename']} (Similarity: {result['similarity_score']:.2f})\n"
                context += "---\n"
                # Optionally load and include document content (commented for now to keep context size manageable)
                # doc_content = _get_document_content(result['index'])
                # if doc_content:
                #     context += doc_content[:500] + "...\n"  # Include first 500 chars
                context += "\n"

    # Build messages with enriched context
    messages_list = []
    for i, msg in enumerate(payload.messages):
        if i == len(payload.messages) - 1:  # Last message (user's current message)
            enriched_content = msg.content
            if context:
                enriched_content = f"{msg.content}\n\n{context}"
            messages_list.append({"role": msg.role, "content": enriched_content})
        else:
            messages_list.append({"role": msg.role, "content": msg.content})

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": payload.model,
        "messages": messages_list,
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
async def get_flight_details_query(
        flight_number: str = Query(..., description="Flight number (e.g., 'LO123', 'FR4567')")):
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
