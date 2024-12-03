from fastapi import APIRouter, Depends, HTTPException
from services.ai_service import AIService
from schemas.chat import ChatRequest, ChatResponse
import json

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    ai_service: AIService = Depends()
):
    try:
        # Get the structured response from the service
        response = await ai_service.generate_response(request.prompt)
        
        # Debug print
        print("Structured response:", json.dumps(response, indent=2))
        
        return ChatResponse(**response)
        
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        ) 