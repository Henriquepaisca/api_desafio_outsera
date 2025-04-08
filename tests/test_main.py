import os
import pytest
import tempfile
import pandas as pd
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from app.main import Base, app, get_db, load_csv_to_db
from app.models import Movie

STATUS_OK = 200

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    db_fd, db_path = tempfile.mkstemp()
    db_url = f"sqlite:///{db_path}"
    
    engine = create_engine(db_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    db = TestingSessionLocal()
    load_csv_to_db(db)
    
    yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_read_root():
    response = client.get("/")
    assert response.status_code == STATUS_OK
    assert response.json() == {'message': 'API para desafio Outsera!'}


def test_get_award_intervals(test_db):

    response = test_db.get("/awards/intervals")
    assert response.status_code == STATUS_OK
    data = response.json()
    assert "min" in data
    assert "max" in data
    if data["min"]:
        producer_min = data["min"][0]
        assert "producer" in producer_min
        assert "interval" in producer_min
        assert "previousWin" in producer_min
        assert "followingWin" in producer_min
    if data["max"]:
        producer_max = data["max"][0]
        assert "producer" in producer_max
        assert "interval" in producer_max
        assert "previousWin" in producer_max
        assert "followingWin" in producer_max
