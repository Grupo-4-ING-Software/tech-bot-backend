from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Resource(BaseModel):
    title: str
    url: str
    type: str

class DiagramNode(BaseModel):
    id: str
    title: str
    description: str
    resources: List[Resource]
    children: Optional[List['DiagramNode']] = None

DiagramNode.model_rebuild()

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[DiagramNode] = None 

class ChatHistory(BaseModel):
    id: UUID
    user_id: int
    prompt: str
    response: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True 