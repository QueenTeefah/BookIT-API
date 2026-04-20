from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.booking import BookingCreate, BookingOut, BookingUpdate
from app.db.session import SessionLocal
from app.services.booking_service import create_booking
from app.utils.dependencies import get_current_user, require_admin
from app.repositories.booking_repo import get_booking_by_id, get_user_bookings, admin_query_bookings

router = APIRouter(prefix="/bookings", tags=["bookings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", status_code=201, response_model=BookingOut)
def create(payload: BookingCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    booking = create_booking(db, current_user.id, payload.service_id, payload.start_time)
    return booking

@router.get("", response_model=list[BookingOut])
def list_bookings(status: str = None, from_date: str = None, to_date: str = None,
                  db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == "admin":
        return admin_query_bookings(db, status=status, from_date=from_date, to_date=to_date)
    return get_user_bookings(db, current_user.id)
