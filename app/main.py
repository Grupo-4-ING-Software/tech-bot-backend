from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, authentication
from core.settings import get_settings
import os

app = FastAPI(title="Tech Career API")
settings = get_settings()

# Configurar CORS
origins = settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(chat.router, prefix="/api") 
app.include_router(authentication.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Tech Career API is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)