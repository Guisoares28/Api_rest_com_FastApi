from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.despesas_crud import criar_nova_despesa, pegar_todas_as_despesas, buscar_despesa_por_id, \
    atualizar_despesa_por_id, deletar_despesa_por_id, buscar_despesa_por_descricao, buscar_despesa_por_mes
from app.database import get_db
from app.exception.despesa_exception import DespesaException
from app.schemas.despesa_schema import DespesaCreate, DespesaResponse


router = APIRouter()

@router.post("/despesas", response_model=DespesaResponse, status_code=201)
def criar_despesa(despesa:DespesaCreate, db:Session = Depends(get_db)):
    try:
        return criar_nova_despesa(despesa=despesa, db=db)
    except DespesaException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/despesas/", response_model=list[DespesaResponse], status_code=200)
def listar_todas_as_despesas(despesa_descricao:str = None ,db:Session = Depends(get_db)):
    if despesa_descricao is None:
        return pegar_todas_as_despesas(db=db)
    try:
        return buscar_despesa_por_descricao(despesa_descricao,db)
    except DespesaException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/despesas/{receita_id}", response_model=DespesaResponse, status_code=200)
def pegar_despesa_por_id(receita_id:int, db:Session = Depends(get_db)):
    return buscar_despesa_por_id(despesa_id=receita_id, db=db)

@router.put("/despesas/{receita_id}", response_model=DespesaResponse, status_code=200)
def atualizar_despesa(despesa_id:int, despesa:DespesaCreate, db:Session = Depends(get_db)):
    return atualizar_despesa_por_id(despesa_id=despesa_id, despesa=despesa, db=db)

@router.delete("/despesas/{despesa_id}", response_model=DespesaResponse, status_code=200)
def deletar_despesa(despesa_id:int, db:Session = Depends(get_db)):
    try:
        return deletar_despesa_por_id(despesa_id=despesa_id, db=db)
    except DespesaException as e:
        HTTPException(status_code=400, detail=str(e))

@router.get("/despesas/{ano}/{mes}", response_model=list[DespesaResponse], status_code=200)
def buscar_despesa_por_mes_e_ano(ano:int, mes:int, db:Session = Depends(get_db)):
    return buscar_despesa_por_mes(mes=mes, ano=ano, db=db)