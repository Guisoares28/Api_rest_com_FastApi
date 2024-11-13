import pytest
from fastapi.testclient import TestClient
from pydantic_core.core_schema import is_instance_schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db, Base
from app.main import app
from app.schemas.receita_schema import ReceitaResponse

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

def test_deve_retornar_todas_as_receitas():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao":"Receita teste",
        "valor": 500.00,
        "data": "2024-11-13"
    }
    response = client.post("/receitas", json=data)
    response = client.get("/receitas")
    receitas = response.json()

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(data["descricao"] == "Receita teste" for receita in receitas)


def test_deve_retornar_uma_receita_pelo_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Receita teste",
        "valor": 500.00,
        "data": "2024-11-13"
    }
    response = client.post("/receitas", json=data)
    id_receita = response.json()["id"]

    response = client.get(f"/receitas/{id_receita}")

    assert response.status_code == 200
    assert response.json()['descricao'] == "Receita teste"

def test_deve_retornar_um_erro_ao_consultar_id_nao_existente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    receita_id = 1
    response = client.get(f"/receitas/{receita_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Receita com Id informado não encontrada"

def test_deve_criar_uma_nova_receita():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Receita teste",
        "valor": 500.00,
        "data": "2024-11-13"
    }
    response = client.post("/receitas", json=data)

    assert response.status_code == 201
    assert response.json()["descricao"] == "Receita teste"

def test_deve_atualizar_receita():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    data = {
        "descricao": "Receita teste",
        "valor": 500.00,
        "data": "2024-11-13"
    }
    response = client.post("/receitas", json=data)
    id_receita = response.json()["id"]
    new_data = {
        "descricao": "Receita atualizada de teste",
        "valor": 10000.00,
        "data": "2025-11-13"
    }
    att_response = client.put(f"/receitas/{id_receita}", json=new_data )

    assert att_response.status_code == 200
    assert att_response.json()["descricao"] == "Receita atualizada de teste"
    assert att_response.json()["valor"] == 10000.00

def test_deve_deletar_uma_conta_pelo_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    data = {
        "descricao": "Receita teste",
        "valor": 500.00,
        "data": "2024-11-13"
    }
    response = client.post("/receitas", json=data)
    id_receita = response.json()["id"]

    delete_response = client.delete(f"/receitas/{id_receita}")

    assert delete_response.status_code == 200
    assert delete_response.json()["descricao"] == "Receita teste"
