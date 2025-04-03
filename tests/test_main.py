from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.main import Base, app, get_db, load_csv_to_db

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

STATUS_OK = 200


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Verifica se a tabela foi criada corretamente
    inspector = inspect(engine).get_table_names()
    assert "movies" in inspector, "Erro: A tabela 'movies' não foi criada!"
    load_csv_to_db(db)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_root():

    response = client.get("/")
    assert response.status_code == STATUS_OK
    assert response.json() == {'message': 'API para desafio Outsera!'}


def test_get_award_intervals(setup_database):

    response = client.get("/awards/intervals")
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
