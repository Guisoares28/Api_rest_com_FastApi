from typing import List
from fastapi import FastAPI, Depends, HTTPException
from models.dependencies.dependencies import SessionLocal
from sqlalchemy.orm import Session
from models.models import Receita
from models.dependencies.conversor import converter_receita_para_receita_response
from Dtos.Receita_DTO import ReceitaResponseDto,ReceitaRequestDto



app = FastAPI()

# Função de dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Função cria uma nova receita, e retorna uma ReceitaResponseDto
@app.post('/receita/criar', response_model= ReceitaResponseDto, status_code=201)
def criar_receita(receita: ReceitaRequestDto, db: Session = Depends(get_db)) -> ReceitaResponseDto:
    receita_existente = db.query(Receita).filter_by(descricao=receita.descricao).first()
    receita_response = converter_receita_para_receita_response(receita_existente)
    if receita_existente:
        if receita_response.data.month == receita.data.month:
            raise HTTPException(status_code=400, detail="Já existe uma receita criada com está descrição.")
    nova_receita = Receita(
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data
    )
    db.add(nova_receita)
    db.commit()
    db.refresh(nova_receita)
    return nova_receita
    
#Função lista todas as receitas do banco de dados, e retorna uma Lista de ReceitaResponseDto
@app.get('/receitas/listar', response_model=List[ReceitaResponseDto], status_code=200)
def listar_receitas(db: Session = Depends(get_db)) -> List[ReceitaResponseDto]:
    receitas = db.query(Receita).all()
    receitas_response = []
    for receita in receitas:
        receita_response = converter_receita_para_receita_response(receita)
        receitas_response.append(receita_response)
    return receitas_response

@app.get('/receitas/<int:receita_id>', response_model=ReceitaResponseDto, status_code=200)
def buscar_receita_por_id(receita_id, db:Session = Depends(get_db)) -> ReceitaResponseDto:
    receita_encontrada = db.query(Receita).filter_by(id=receita_id).first()
    receita_response = converter_receita_para_receita_response(receita_encontrada)
    if not receita_response:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return receita_response

@app.put('/receitas/update/<int:receita_id>', response_model=ReceitaResponseDto, status_code=200)
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

@app.delete('/receita/delete/<int:receita_id>', status_code=200 )
def deletar_receita(receita_id, db:Session=Depends(get_db)):
    db.query(Receita).filter_by(id=receita_id).delete()
    db.commit()
    response = {
        'message':'Receita deletada com sucesso!'
    }
    return response




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)