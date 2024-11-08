from calendar import day_abbr

import pytest
import pytest_asyncio
from httpx import AsyncClient
from app import app
import sqlite3


sql_script = (
    """CREATE TABLE IF NOT EXISTS receitas(
            id integer primary key autoincrement,
            descricao varchar(200) not null,
            valor real not null,
            data date not null
            );
""")


def conectar_bd_teste():
    conn = sqlite3.connect('C://Users//Guilherme//Desktop//Projetos//Alura_challenger/test.db')
    return conn

@pytest.fixture(scope="function")
def criar_banco():
    with conectar_bd_teste() as db:
        db.cursor().executescript("DROP TABLE IF EXISTS receitas;")
        db.cursor().executescript(sql_script)
    db.commit()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_cria_uma_receita_e_retorna_um_receitaresponsedto(client, criar_banco):
    data = {
        "descricao": "Receita de teste",
        "valor": 500.00,
        "data": "2024-11-08"
    }
    response = await client.post("/receita/criar", json=data)
    assert response.status_code == 201
    assert response.json()["descricao"] == "Receita de teste"
    assert response.json()["valor"] == 500.00
    assert response.json()["data"] == "2024-11-08"

    response = await client.post("/receita/criar", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Já existe uma receita criada com está descrição."

@pytest.mark.asyncio
async def test_retorna_uma_lista_de_receitaresponsedto(client, criar_banco):
    response = await client.get('/receitas/listar')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_buscar_receita_por_id(client, criar_banco):
    data = {
        "descricao":"conta teste",
        "valor":500.00,
        "data":"2024-11-08"
    }
    response = await client.post("/receita/criar", json=data)
    receita_id : int = response.json()['id']

    response = await client.get(f'/receitas/{receita_id}')
    assert response.status_code == 200
    assert response.json()['descricao'] == "conta teste"
    assert response.json()['valor'] == 500.00
    assert response.json()['data'] == "2024-11-08"

@pytest.mark.asyncio
async def test_deve_retornar_uma_resposta_404_not_found_ao_tentar_buscar_um_id_inexistente(client, criar_banco):
    receita_id : int = 999
    response = await client.get(f'/receitas/{receita_id}')
    assert response.status_code == 404
    assert response.json()["detail"] == "Receita não encontrada"


@pytest.mark.asyncio
async def test_atualizacao_de_receita(client, criar_banco):
    data = {
        "descricao": "conta teste",
        "valor": 500.00,
        "data": "2024-11-08"
    }
    response = await client.post("/receita/criar", json=data)
    receita_id: int = response.json()['id']

    data_atualizado = {
        "descricao": "conta teste atualizada",
        "valor":1000.00,
        "data":"2024-12-11"
    }
    response = await client.put(f'/receitas/update/{receita_id}', json=data_atualizado)

    assert response.status_code == 200
    assert response.json()['descricao'] == "conta teste atualizada"
    assert response.json()['valor'] == 1000.00
    assert response.json()['data'] == "2024-12-11"


@pytest.mark.asyncio
async def test_deletar_receita(client, criar_banco):
    data = {
        "descricao": "conta teste",
        "valor": 500.00,
        "data": "2024-11-08"
    }
    response = await client.post("/receita/criar", json=data)
    receita_id: int = response.json()['id']

    response = await client.delete(f'/receita/delete/{receita_id}')

    assert response.status_code == 200
    assert response.json()["message"] == "Receita deletada com sucesso!"

