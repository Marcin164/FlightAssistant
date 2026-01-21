from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import importlib

app = FastAPI()

# Configure CORS
origins = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    """Simple health endpoint."""
    return {"status": "ok"}

# Register routers dynamically to avoid static import issues in some tools
try:
    openai_module = importlib.import_module("routers.openai")
    openai_router = getattr(openai_module, "router")
    app.include_router(openai_router, prefix="/api/openai")
except Exception:
    # In development or static analysis environments this may fail; ignore so tooling doesn't break.
    pass
