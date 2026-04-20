from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.services import service_service
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/services", tags=["Services"])

# 🟢 Public — Get all services (search + filters)
@router.get("/", response_model=List[ServiceResponse])
def list_services(
    q: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return service_service.list_services(db, q, price_min, price_max, active)


# 🟢 Public — Get single service by ID
@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    return service_service.get_service_by_id(db, service_id)


# 🔒 Admin only — Create new service
@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return service_service.create_service(db, service_data)


# 🔒 Admin only — Update a service
@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    update_data: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return service_service.update_service(db, service_id, update_data)


# 🔒 Admin only — Delete a service
@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    service_service.delete_service(db, service_id)
    return
