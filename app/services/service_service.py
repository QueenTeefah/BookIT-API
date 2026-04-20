from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import service_repo
from app.schemas.service import ServiceCreate, ServiceUpdate

# ✅ Create new service (admin)
def create_service(db: Session, service_data: ServiceCreate):
    new_service = service_repo.create_service(db, service_data)
    return new_service


# ✅ Get all services (public + filter options)
def list_services(db: Session, q=None, price_min=None, price_max=None, active=None):
    services = service_repo.get_services(db, q, price_min, price_max, active)
    return services


# ✅ Get single service by ID
def get_service_by_id(db: Session, service_id: int):
    service = service_repo.get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service


# ✅ Update service (admin)
def update_service(db: Session, service_id: int, update_data: ServiceUpdate):
    updated = service_repo.update_service(db, service_id, update_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return updated


# ✅ Delete service (admin)
def delete_service(db: Session, service_id: int):
    deleted = service_repo.delete_service(db, service_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return {"message": "Service deleted successfully"}
