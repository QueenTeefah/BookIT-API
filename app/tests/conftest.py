import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.db.session import SessionLocal, engine
from app.db.base import Base

@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    app = create_app()
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
