from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class BookingStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class BookingCreate(BaseModel):
    service_id: int
    start_time: datetime

class BookingUpdate(BaseModel):
    start_time: Optional[datetime]
    status: Optional[BookingStatus]

class BookingOut(BaseModel):
    id: int
    user_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True

