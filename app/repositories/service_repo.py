from sqlalchemy.orm import Session
from app.models.services import Service

# Create service
def create_service(db: Session, service_data):
    new_service = Service(**service_data.dict())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

# Get all services (with optional filters)
def get_services(db: Session, q=None, price_min=None, price_max=None, active=None):
    query = db.query(Service)
    if q:
        query = query.filter(Service.title.ilike(f"%{q}%"))
    if price_min:
        query = query.filter(Service.price >= price_min)
    if price_max:
        query = query.filter(Service.price <= price_max)
    if active is not None:
        query = query.filter(Service.is_active == active)
    return query.all()

# Get service by ID
def get_service_by_id(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()

# Update service
def update_service(db: Session, service_id: int, update_data):
    service = get_service_by_id(db, service_id)
    if not service:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service

# Delete service
def delete_service(db: Session, service_id: int):
    service = get_service_by_id(db, service_id)
    if service:
        db.delete(service)
        db.commit()
        return True
    return False
