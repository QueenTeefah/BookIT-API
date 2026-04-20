from sqlalchemy.orm import Session
from app.models.review import Review

# Create a new review
def create_review(db: Session, review_data):
    new_review = Review(**review_data.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Get reviews for a specific service
def get_reviews_for_service(db: Session, service_id: int):
    return db.query(Review).filter(Review.booking_id == service_id).all()

# Get review by ID
def get_review_by_id(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

# Update review
def update_review(db: Session, review_id: int, update_data):
    review = get_review_by_id(db, review_id)
    if not review:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(review, key, value)
    db.commit()
    db.refresh(review)
    return review

# Delete review
def delete_review(db: Session, review_id: int):
    review = get_review_by_id(db, review_id)
    if review:
        db.delete(review)
        db.commit()
        return True
    return False
