from pydantic import BaseModel
from typing import Optional, List

class CreateResourceRequestSchema(BaseModel):
    name: str
    properties: dict

class UpdateResourceRequestSchema(BaseModel):
    properties: Optional[dict] = None

class CreateResourceResponseSchema(BaseModel):
    resourceId: str
    name: str
    properties: dict

class GetResourceResponseSchema(BaseModel):
    resourceId: str
    name: str
    properties: dict

class GetAllResourcesResponseSchema(BaseModel):
    items: List[GetResourceResponseSchema]
    total: int
