from http.client import responses

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app
from app.schemas.despesa_schema import Categoria

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

def test_deve_retornar_um_erro_ao_tentar_salvar_despesa_com_mesmo_nome():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Despesa Teste",
        "valor": 20000.00,
        "data": "2024-11-13"
    }
    response = client.post("/despesas", json=data)

    data_two = {
        "descricao": "Despesa Teste",
        "valor": 40.00,
        "data": "2024-11-10"
    }
    response = client.post("/despesas", json=data_two)

    assert response.status_code == 400
    assert response.json()["detail"] == "400: Despesa já Cadastrada"

def test_deve_retornar_uma_despesa_por_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Despesa Teste",
        "valor": 20000.00,
        "data": "2024-11-13"
    }
    response = client.post("/receitas", json=data)
    receita_id = response.json()["id"]
    response_two = client.get(f"/receitas/{receita_id}")

    assert response_two.json()["descricao"] == "Despesa Teste"
    assert response_two.json()["valor"] == 20000.00
    assert response_two.json()["data"] == "2024-11-13"

def test_deve_retornar_a_categoria_padrao_caso_nao_seja_informado():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Despesa Teste",
        "valor": 20000.00,
        "data": "2024-11-13"
    }
    response = client.post("/despesas", json=data)
    assert response.json()["categoria"] == "outras"
    assert isinstance(response.json()["categoria"], str)

def test_deve_retornar_uma_despesa_pela_descricao():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Despesa Teste",
        "valor": 20000.00,
        "data": "2024-11-13"
    }
    response = client.post("/despesas", json=data)
    descricao = response.json()["descricao"]
    response_two = client.get(f"/despesas/?despesa_descricao={descricao}")
    assert response_two.status_code == 200
    assert response_two.json()[0]["descricao"] == "Despesa Teste"
