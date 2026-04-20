from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


# ✅ Shared fields for both create & update
class ServiceBase(BaseModel):
    title: str = Field(..., example="Luxury Spa Package")
    description: str = Field(..., example="Full body massage and aromatherapy session")
    price: float = Field(..., gt=0, example=25000.0)
    duration_minutes: int = Field(..., gt=0, example=90)
    is_active: Optional[bool] = True


# ✅ Schema for creating a service (admin)
class ServiceCreate(ServiceBase):
    pass


# ✅ Schema for updating a service (admin)
class ServiceUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    duration_minutes: Optional[int]
    is_active: Optional[bool]


# ✅ Schema for reading service data (response)
class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

