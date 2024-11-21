from typing import List, Optional
from pydantic import BaseModel

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