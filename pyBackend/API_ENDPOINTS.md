# Flight Assistant Backend API - Dokumentacja Endpointów

## Adres Bazowy
```
http://localhost:8000
```

## Dostępne Endpointy

### 1. Chat (Chat z OpenAI)

**POST** `/api/openai/chat`

Wysłanie wiadomości do OpenAI i otrzymanie odpowiedzi.

**Request Body:**
```json
{
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": "Ile dni trwa podróż z Warszawy do Londynu?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

**Response:**
```json
{
  "reply": "Podróż z Warszawy do Londynu zajmuje około 2-3 dni...",
  "raw": { /* pełna odpowiedź OpenAI */ }
}
```

**cURL Przykład:**
```bash
curl -X POST http://localhost:8000/api/openai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Ile dni trwa podróż z Warszawy do Londynu?"
      }
    ]
  }'
```

---

### 2. Szczegóły Lotu - POST

**POST** `/api/openai/flight-details`

Uzyskiwanie szczegółów lotu na podstawie numeru lotu (metoda POST).

**Request Body:**
```json
{
  "flight_number": "LO123"
}
```

**Response:**
```json
{
  "flightNumber": "LO123",
  "airline": "LOT Polish Airlines",
  "from": "Warsaw Chopin",
  "to": "London Heathrow",
  "departureTime": "14:30",
  "arrivalTime": "15:45",
  "gate": "A12",
  "terminal": "1",
  "status": "On Time",
  "delayMinutes": null
}
```

**cURL Przykład:**
```bash
curl -X POST http://localhost:8000/api/openai/flight-details \
  -H "Content-Type: application/json" \
  -d '{"flight_number": "LO123"}'
```

---

### 3. Szczegóły Lotu - GET

**GET** `/api/openai/flight-details?flight_number=LO123`

Uzyskiwanie szczegółów lotu na podstawie numeru lotu (metoda GET).

**Query Parameters:**
- `flight_number` (wymagane): Numer lotu, np. "LO123", "FR4567"

**Response:**
```json
{
  "flightNumber": "LO123",
  "airline": "LOT Polish Airlines",
  "from": "Warsaw Chopin",
  "to": "London Heathrow",
  "departureTime": "14:30",
  "arrivalTime": "15:45",
  "gate": "A12",
  "terminal": "1",
  "status": "On Time",
  "delayMinutes": null
}
```

**cURL Przykład:**
```bash
curl http://localhost:8000/api/openai/flight-details?flight_number=LO123
```

---

### 4. Health Check

**GET** `/health`

Sprawdzenie statusu serwera.

**Response:**
```json
{
  "status": "ok"
}
```

---

## Konfiguracja CORS

Aby frontend mógł komunikować się z backendem, musisz skonfigurować CORS w pliku `.env`:

```dotenv
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
```

## Potrzebne Zmienne Środowiskowe

Utwórz plik `.env` na podstawie `.env.example`:

```dotenv
OPENAI_API_KEY=your-openai-key-here
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Uruchomienie Serwera

```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom serwer
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testowanie z Frontendu

### JavaScript/TypeScript (Fetch API):

```javascript
// Chat endpoint
const chatResponse = await fetch('http://localhost:8000/api/openai/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [
      { role: 'user', content: 'Cześć!' }
    ]
  })
});
const chatData = await chatResponse.json();
console.log(chatData.reply);

// Flight details endpoint (GET)
const flightResponse = await fetch('http://localhost:8000/api/openai/flight-details?flight_number=LO123');
const flightData = await flightResponse.json();
console.log(flightData);

// Flight details endpoint (POST)
const flightResponse = await fetch('http://localhost:8000/api/openai/flight-details', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ flight_number: 'LO123' })
});
const flightData = await flightResponse.json();
console.log(flightData);
```

### Python (requests):

```python
import requests

# Chat endpoint
response = requests.post('http://localhost:8000/api/openai/chat', json={
    'messages': [
        {'role': 'user', 'content': 'Cześć!'}
    ]
})
print(response.json()['reply'])

# Flight details endpoint
response = requests.get('http://localhost:8000/api/openai/flight-details?flight_number=LO123')
print(response.json())
```

## Obsługiwane Statusy Lotów

- `On Time` - Na czas
- `Delayed` - Opóźniony
- `Boarding` - Wchodzenie na pokład
- `Cancelled` - Odwołany

## Błędy

- **400 Bad Request**: Niepoprawny format żądania
- **500 Internal Server Error**: Klucz API OpenAI nie skonfigurowany
- **502 Bad Gateway**: Błąd komunikacji z OpenAI API


