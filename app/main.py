from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, authentication
from app.core.settings import get_settings

app = FastAPI()
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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}