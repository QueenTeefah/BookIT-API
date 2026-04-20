from pydantic import BaseModel , Field
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    booking_id: int
    rating: int
    comment: Optional[str]

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=255)


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: Optional[str]
    service_id: int
    user_id: int
    created_at: datetime

class ReviewOut(BaseModel):
    id: int
    booking_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

