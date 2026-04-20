from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_db: User, changes: UserUpdate) -> User:
    for k, v in changes.dict(exclude_unset=True).items():
        setattr(user_db, k, v)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db
