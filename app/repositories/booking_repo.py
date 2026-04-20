from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import timedelta
from app.models.booking import Booking
from app.models.services import Service


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_user_bookings(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

def admin_query_bookings(db: Session):
    return db.query(Booking).all()


def get_booking_conflicts(db: Session, service_id: int, start_time, end_time):
    # If any booking for the same service where times overlap and status != cancelled
    q = db.query(Booking).filter(
        Booking.service_id == service_id,
        Booking.status != "cancelled",
        or_(
            and_(Booking.start_time <= start_time, Booking.end_time > start_time),
            and_(Booking.start_time < end_time, Booking.end_time >= end_time),
            and_(Booking.start_time >= start_time, Booking.end_time <= end_time),
        )
    )
    return q.all()
