import httpx
import json
import os
import pandas as pd
import pickle
from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from pydantic import BaseModel, Field
from scripts.vektorizer import DocumentVectorizer
from typing import List, Optional, Any, Dict

_vector_db = DocumentVectorizer()

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
XRAPID_KEY = os.getenv("XRAPID_KEY")
if not OPENAI_API_KEY:
    # In production you should fail fast or ensure env is configured via secrets manager
    OPENAI_API_KEY = ""
    XRAPID_KEY = ""

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


def _search_vectors(query: str, top_k: int = 5):
    df = _vector_db.search(query=query, top_k=top_k)
    return df.to_dict("records")


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
    temperature: Optional[float] = 0.8
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


@router.on_event("startup")
def load_vector_db():
    _vector_db.load("./scripts/vectors_db")

    documents = []

    for meta in _vector_db.metadata:
        try:
            with open(meta["path"], "r", encoding="utf-8") as f:
                content = f.read().strip()
                chunks = _vector_db.chunk_text(content)

                # safety check
                if meta["chunk_id"] < len(chunks):
                    documents.append(chunks[meta["chunk_id"]])
                else:
                    documents.append("")
        except Exception as e:
            print(f"❌ Failed loading chunk: {e}")
            documents.append("")

    _vector_db.documents = documents

    print(f"✅ Vector DB ready: {len(_vector_db.documents)} chunks loaded")


@router.post("/chat", response_model=ChatResponse)
async def chat_proxy(payload: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    user_message = payload.messages[-1].content

    #ROUTE INTENT
    intent = await classify_user_intent(user_message)

    context_blocks = []

    #VECTOR SEARCH (if needed)
    if intent["needs_vector_search"]:
        results = _search_vectors(user_message, top_k=5)
        if results:
            context = "\n### KNOWLEDGE BASE CHUNKS ###\n"
            for r in results:
                chunk = _vector_db.documents[r["index"]]
                context += (
                    f"\n[Source: {r['filename']} | chunk {r['chunk_id']}]\n"
                    f"{chunk}\n"
                )
            context_blocks.append(context)

    #FLIGHT LOOKUP (if needed)
    if intent["needs_flight_lookup"] and intent["flight_number"]:
        flight_data = await get_flight_details_external(intent["flight_number"])
        if flight_data:
            context_blocks.append(
                "\n### FLIGHT INFORMATION ###\n"
                + json.dumps(flight_data, indent=2, ensure_ascii=False)
            )

    messages = [{
        "role": "system",
        "content": (
            "You are an aviation assistant.\n\n"
            "Rules:\n"
            "- If document context is present, base the answer on it and cite airline rules.\n"
            "- If not found in documents, say so and use general aviation knowledge.\n"
            "- If flight data is present, explain it clearly to the user.\n\n"
            + "\n".join(context_blocks)
        )
    }]

    messages.extend([msg.dict() for msg in payload.messages])

    #FINAL CALL (better model)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    body = {
        "model": "gpt-4o",  # stronger reasoning model
        "messages": messages,
        "temperature": payload.temperature,
        "max_tokens": payload.max_tokens,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, headers=headers)

    data = resp.json()
    reply = data["choices"][0]["message"]["content"]

    return ChatResponse(reply=reply, raw=data)



async def classify_user_intent(text: str) -> Dict[str, Any]:
    """Use a fast LLM to decide what tools are needed."""
    url = "https://api.openai.com/v1/chat/completions"

    system_prompt = """
You are a routing assistant.
Analyze the user message and decide:

1. Does it require searching aviation regulations documents?
2. Does it contain a flight number (e.g. LO123, FR4567)?

Respond ONLY with valid JSON in this format:
{
  "needs_vector_search": boolean,
  "needs_flight_lookup": boolean,
  "flight_number": string | null
}
"""

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        "temperature": 0.0,
        "max_tokens": 200
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.post(url, json=body, headers=headers)

    data = resp.json()
    return json.loads(data["choices"][0]["message"]["content"])

async def get_flight_details_external(flight_number: str) -> Dict[str, Any]:
    url = f"https://aerodatabox.p.rapidapi.com/flights/number/{flight_number}"

    headers = {
        "x-rapidapi-key": XRAPID_KEY,
        "x-rapidapi-host": "aerodatabox.p.rapidapi.com",
    }

    params = {
        "withAircraftImage": False,
        "withLocation": True,
        "withFlightPlan": False,
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(url, headers=headers, params=params)

    if resp.status_code != 200:
        return {}

    data = resp.json()
    return data[0] if data else {}


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


@router.get("/airports", response_model=Dict[str, Any])
async def testEndpoint(
        airport_name: str = Query(..., description="Input text to search airports in")
):
    file_path = Path(__file__).parent / "airports.json"

    with open(file_path, "r", encoding="utf-8") as f:
        airports = json.load(f)

    airport_name_lower = airport_name.lower()
    airports_to_return = []

    for airport in airports:
        name = airport.get("name")

        # skip missing or invalid names
        if not isinstance(name, str):
            continue

        airport_name = name.lower()

        if airport_name_lower in airport_name:
            airports_to_return.append(airport)

    return {
        "airports": airports_to_return
    }


@router.get("/test", response_model=Dict[str, Any])
async def testEndpoint(
        text: str = Query(..., description="Input text to search airports in")
):
    return {
        "text": text
    }
