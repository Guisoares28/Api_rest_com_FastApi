from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app

client = TestClient(app)

DATABASE_ALCHEMY_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_ALCHEMY_URL, connect_args= {"check_same_thread":False})

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_deve_criar_uma_nova_despesa():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Despesa Teste",
        "valor": 20000.00,
        "data": "2024-11-13"
    }
    response = client.post("/despesas", json=data)

    assert response.status_code == 201
    assert response.json()["descricao"] == "Despesa Teste"
