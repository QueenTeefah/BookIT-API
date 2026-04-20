from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.repositories import booking_repo, service_repo
from app.models.booking import Booking, BookingStatus

def create_booking(db: Session, user_id: int, service_id: int, start_time):
    service = service_repo.get_service(db, service_id)
    if not service or not service.is_active:
        raise HTTPException(status_code=404, detail="Service not found")
    end_time = start_time + timedelta(minutes=service.duration_minutes)
    conflicts = booking_repo.get_booking_conflicts(db, service_id, start_time, end_time)
    if conflicts:
        raise HTTPException(status_code=409, detail="Booking conflict")
    booking = Booking(user_id=user_id, service_id=service_id, start_time=start_time, end_time=end_time)
    db.add(booking); db.commit(); db.refresh(booking)
    return booking
