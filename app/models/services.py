from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10,2), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookings = relationship("Booking", back_populates="service", cascade="all, delete-orphan")
    reviews = relationship(
        "Review",
        secondary="bookings",
        primaryjoin="Service.id==Booking.service_id",
        secondaryjoin="Booking.id==Review.booking_id",
        viewonly=True,
    )
