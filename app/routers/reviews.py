from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from app.repositories import review_repo, booking_repo
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/reviews", tags=["Reviews"])

# Create a review (user only, for completed booking)
@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review_data: ReviewCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Check that booking exists and belongs to current user
    booking = booking_repo.get_booking_by_id(db, review_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your booking")
    if booking.status != "completed":
        raise HTTPException(status_code=400, detail="Can only review completed bookings")

    # Check if review already exists for that booking
    existing = db.query(review_repo.Review).filter_by(booking_id=review_data.booking_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Review already exists for this booking")

    new_review = review_repo.create_review(db, review_data)
    return new_review


# Get reviews for a specific service
@router.get("/service/{service_id}", response_model=list[ReviewResponse])
def get_reviews_for_service(service_id: int, db: Session = Depends(get_db)):
    reviews = review_repo.get_reviews_for_service(db, service_id)
    return reviews


# Update review (only owner)
@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, update_data: ReviewUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    review = review_repo.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    updated = review_repo.update_review(db, review_id, update_data)
    return updated


# Delete review (owner or admin)
@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    review = review_repo.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Only owner or admin can delete
    if current_user.role != "admin" and review.booking.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    review_repo.delete_review(db, review_id)
    return
