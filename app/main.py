from fastapi import FastAPI, Request
from app.core.config import settings
from app.core.logging import logger
from app.routers import auth, services, bookings, users, reviews
from app.db.session import engine
from app.db.base import Base

def create_app():
    app = FastAPI(title=settings.APP_NAME)
    # create tables in dev (production use alembic)
    Base.metadata.create_all(bind=engine)
    app.include_router(auth.router)
    app.include_router(services.router)
    app.include_router(bookings.router)
    # users, reviews similarly
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"Incoming request {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Completed {request.method} {request.url} -> {response.status_code}")
        return response

    return app

app = create_app()
