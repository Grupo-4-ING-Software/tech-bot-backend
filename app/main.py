from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, authentication

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api") 
app.include_router(authentication.router, prefix="/api")