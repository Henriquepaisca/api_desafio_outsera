import os
import pytest
import tempfile
import pandas as pd
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from pathlib import Path

from app.main import Base, app, get_db, load_csv_to_db, CSV_PATH
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

    assert isinstance(data["max"], dict)
    assert isinstance(data["min"], dict)

    for key in ["producer", "interval", "previousWin", "followingWin"]:
        assert key in data["max"]
        assert key in data["min"]

    assert data["max"]["producer"] == "Matthew Vaughn"
    assert data["max"]["interval"] == 13
    assert data["max"]["previousWin"] == 2002
    assert data["max"]["followingWin"] == 2015

    assert data["min"]["producer"] == "Joel Silver"
    assert data["min"]["interval"] == 1
    assert data["min"]["previousWin"] == 1990
    assert data["min"]["followingWin"] == 1991


import pandas as pd

def test_csv_headers():
    headers = ["year", "title", "studios", "producers", "winner"]
    df = pd.read_csv(CSV_PATH, sep=";", nrows=0)

    actual_headers = df.columns.tolist()

    assert actual_headers == headers, f"Headers incorretos. Esperado: {headers}, Encontrado: {actual_headers}"
