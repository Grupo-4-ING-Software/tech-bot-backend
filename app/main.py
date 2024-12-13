from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, authentication

app = FastAPI()

# Configurar CORS
origins = [
    "http://localhost:5173",  # Tu frontend React
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
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
app.include_router(chat.router, prefix="/api") 
app.include_router(authentication.router, prefix="/api")