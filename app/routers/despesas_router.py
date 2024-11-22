from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.despesas_crud import DespesaCrud
from app.database import get_db
from app.depends import token_verifier
from app.exception.despesa_exception import DespesaException
from app.schemas.despesa_schema import DespesaCreate, DespesaResponse


router = APIRouter(prefix="/despesas", dependencies=[Depends(token_verifier)])

@router.post("/criar", response_model=DespesaResponse, status_code=201)
def criar_despesa(despesa:DespesaCreate, db:Session = Depends(get_db)):
    dc = DespesaCrud(db=db)
    try:
        return dc.criar_nova_despesa(despesa=despesa)
    except DespesaException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/listar/", response_model=list[DespesaResponse], status_code=200)
def listar_todas_as_despesas(despesa_descricao:str = None ,db:Session = Depends(get_db)):
    dc = DespesaCrud(db=db)
    if despesa_descricao is None:
        return dc.pegar_todas_as_despesas()
    try:
        return dc.buscar_despesa_por_descricao(despesa_descricao)
    except DespesaException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/buscar/{receita_id}", response_model=DespesaResponse, status_code=200)
def pegar_despesa_por_id(receita_id:int, db:Session = Depends(get_db)):
    dc = DespesaCrud(db=db)
    return dc.buscar_despesa_por_id(despesa_id=receita_id)

@router.put("/atualizar/{receita_id}", response_model=DespesaResponse, status_code=200)
def atualizar_despesa(despesa_id:int, despesa:DespesaCreate, db:Session = Depends(get_db)):
    dc = DespesaCrud(db=db)
    return dc.atualizar_despesa_por_id(despesa_id=despesa_id, despesa=despesa)

@router.delete("/deletar/{despesa_id}", response_model=DespesaResponse, status_code=200)
def deletar_despesa(despesa_id:int, db:Session = Depends(get_db)):
    dc = DespesaCrud(db=db)
    try:
        return dc.deletar_despesa_por_id(despesa_id=despesa_id)
    except DespesaException as e:
        HTTPException(status_code=400, detail=str(e))

@router.get("/buscar_mes/{ano}/{mes}", response_model=list[DespesaResponse], status_code=200)
def buscar_despesa_por_mes_e_ano(ano:int, mes:int, db:Session = Depends(get_db)):
    dc = DespesaCrud(db=db)
    return dc.buscar_despesa_por_mes(mes=mes, ano=ano)