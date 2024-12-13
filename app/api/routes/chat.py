from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from services.ai_service import AIService
from schemas.chat import ChatRequest, ChatResponse, ChatHistory
from models.chat import ChatHistory as ChatHistoryModel
from services.database_connection_service import get_db
from api.routes.authentication import verify_token
from uuid import UUID
import json
from datetime import datetime

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    ai_service: AIService = Depends(),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    try:
        # Get the structured response from the service
        response = await ai_service.generate_response(request.prompt)
        
        # Create a new chat history entry
        chat_history = ChatHistoryModel(
            user_id=current_user["user_id"],
            prompt=request.prompt,
            response=response,
            created_at=datetime.utcnow()
        )
        
        # Save to database
        try:
            db.add(chat_history)
            db.commit()
            db.refresh(chat_history)
        except Exception as db_error:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(db_error)}"
            )
        
        # Return the response
        return ChatResponse(data=response['data'])
        
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

@router.get("/chat/history", response_model=List[ChatHistory])
async def get_chat_history(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all chat history for the current user"""
    try:
        print(f"Getting chat history for user_id: {current_user.get('user_id')}")
        
        # Verificar que user_id existe
        if not current_user.get("user_id"):
            raise HTTPException(
                status_code=400,
                detail="User ID not found in token"
            )

        # Obtener chats
        chats = db.query(ChatHistoryModel).filter(
            ChatHistoryModel.user_id == current_user["user_id"]
        ).order_by(ChatHistoryModel.created_at.desc()).all()
        
        # Procesar cada chat
        processed_chats = []
        for chat in chats:
            try:
                # Asegurarse que response es un dict
                if isinstance(chat.response, str):
                    chat.response = json.loads(chat.response)
                elif not isinstance(chat.response, dict):
                    chat.response = {}
                
                processed_chats.append(chat)
            except json.JSONDecodeError as e:
                print(f"Error processing chat {chat.id}: {str(e)}")
                # Skip invalid chats
                continue
        
        return processed_chats

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_chat_history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )

@router.get("/chat/{chat_id}", response_model=ChatHistory)
async def get_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get a specific chat by ID"""
    try:
        chat = db.query(ChatHistoryModel).filter(
            ChatHistoryModel.id == chat_id,
            ChatHistoryModel.user_id == current_user["user_id"]
        ).first()
        
        if not chat:
            raise HTTPException(
                status_code=404,
                detail="Chat not found"
            )
        
        # Verificar que la respuesta sea serializable
        if not isinstance(chat.response, dict):
            chat.response = json.loads(chat.response) if isinstance(chat.response, str) else {}
        
        return chat
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat: {str(e)}"
        )

@router.delete("/chat/{chat_id}")
async def delete_chat(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Delete a specific chat"""
    chat = db.query(ChatHistoryModel).filter(
        ChatHistoryModel.id == chat_id,
        ChatHistoryModel.user_id == current_user["user_id"]
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=404,
            detail="Chat not found"
        )
        
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}

@router.delete("/chat/history/all")
async def delete_all_chats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Delete all chats for the current user"""
    db.query(ChatHistoryModel).filter(
        ChatHistoryModel.user_id == current_user["user_id"]
    ).delete()
    db.commit()
    return {"message": "All chats deleted successfully"} 