from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterIn, LoginIn, Token
from app.db.session import SessionLocal
from app.services.auth_service import register_user, login_user
from app.utils.security import create_access_token, create_refresh_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", status_code=201, response_model=Token)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload.name, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    auth = login_user(db, payload.email, payload.password)
    return {"access_token": auth["access_token"], "refresh_token": auth["refresh_token"]}

@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    auth = login_user(db, payload.email, payload.password)
    if not auth:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": auth["access_token"], "refresh_token": auth["refresh_token"]}
