from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.service import ServiceOut, ServiceCreate, ServiceUpdate
from app.db.session import SessionLocal
from app.repositories import service_repo
from app.utils.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/services", tags=["services"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[ServiceOut])
def list_services(q: str = None, price_min: float = None, price_max: float = None,
                  active: bool = True, db: Session = Depends(get_db)):
    services = service_repo.query_services(db=db, q=q, price_min=price_min, price_max=price_max, active=active)
    return services

@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    svc = service_repo.get_service(db, service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    return svc

@router.post("", status_code=201, dependencies=[Depends(require_admin)], response_model=ServiceOut)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    svc = service_repo.create_service(db, payload)
    return svc

@router.patch("/{service_id}", dependencies=[Depends(require_admin)], response_model=ServiceOut)
def update_service(service_id: int, payload: ServiceUpdate, db: Session = Depends(get_db)):
    svc = service_repo.get_service(db, service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    svc = service_repo.update_service(db, svc, payload)
    return svc

@router.delete("/{service_id}", status_code=204, dependencies=[Depends(require_admin)])
def delete_service(service_id: int, db: Session = Depends(get_db)):
    svc = service_repo.get_service(db, service_id)
    if not svc:
        raise HTTPException(status_code=404, detail="Service not found")
    service_repo.delete_service(db, svc)
    return None
