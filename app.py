from http.client import HTTPResponse
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.orm import Session
from models.models import Receita
from dto.receita_dto import ReceitaResponseDto,ReceitaRequestDto
from models.dependencies.dependencies import get_db
from service.receita_service import  buscar_receita_por_id, \
    salvar_receita_no_banco_de_dados, buscar_todas_as_receitas_do_banco

app = FastAPI()

# Função de dependência para obter a sessão do banco



#Função cria uma nova receita, e retorna uma ReceitaResponseDto
@app.post('/receita/criar', response_model= ReceitaResponseDto, status_code=201)
def criar_receita(receita: ReceitaRequestDto, db: Session = Depends(get_db)) -> ReceitaResponseDto:
    return salvar_receita_no_banco_de_dados(receita)
    
#Função lista todas as receitas do banco de dados, e retorna uma Lista de ReceitaResponseDto
@app.get('/receitas/listar', response_model=List[ReceitaResponseDto], status_code=200)
def listar_receitas(db: Session = Depends(get_db)) -> List[ReceitaResponseDto]:
    return buscar_todas_as_receitas_do_banco()

#Função que recebe um Id no URL e retorna a receita encontrada.
@app.get('/receitas/{receita_id}', response_model=ReceitaResponseDto, status_code=200)
def buscar_receita_by_id(receita_id, db:Session = Depends(get_db)) -> ReceitaResponseDto:
    receita_encontrada = buscar_receita_por_id(receita_id)
    if not receita_encontrada:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return buscar_receita_por_id(receita_id)

#Função que recebe um id na URL e atualiza uma receita
@app.put('/receitas/update/{receita_id}', response_model=ReceitaResponseDto, status_code=200)
def atualizar_receita(receita_id, receita: ReceitaRequestDto, db:Session= Depends(get_db)) -> ReceitaResponseDto:
    receita_encontrada = db.query(Receita).filter_by(id=receita_id).first()
    if not receita_encontrada:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    receita_encontrada.descricao = receita.descricao
    receita_encontrada.valor = receita.valor
    receita_encontrada.data = receita.data
    db.add(receita_encontrada)
    db.commit()
    db.refresh(receita_encontrada)
    receita_response = converter_receita_para_receita_response(receita_encontrada)
    return receita_response

#Função que deleta uma receita recebendo um Id na URL
@app.delete('/receita/delete/{receita_id}', status_code=200 )
def deletar_receita(receita_id, db:Session=Depends(get_db)):
    receita_encontrada = db.query(Receita).filter_by(id=receita_id).first()
    if receita_encontrada:
        db.delete(receita_encontrada)
    else:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    db.commit()
    response = {
        'message': 'Receita deletada com sucesso!'
    }
    return response




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)