from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserOut, UserUpdate,Role
from app.repositories.user_repo import get_user_by_email, update_user
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# Get current user profile
@router.get("/me", response_model=UserOut)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


# Update current user profile
@router.patch("/me", response_model=UserOut)
def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated = update_user(db, current_user.id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
