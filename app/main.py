from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, authentication
from app.core.settings import get_settings

app = FastAPI()
settings = get_settings()

# Configurar CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(authentication.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}