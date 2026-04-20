from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServiceCreate(BaseModel):
    title: str
    description: Optional[str]
    price: float
    duration_minutes: int
    is_active: Optional[bool] = True

class ServiceUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    duration_minutes: Optional[int]
    is_active: Optional[bool]

class ServiceOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: float
    duration_minutes: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

