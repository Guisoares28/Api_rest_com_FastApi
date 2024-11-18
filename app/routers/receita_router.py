from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.crud.receitas_crud import pegar_todas_as_receitas, pegar_receita_por_id, salvar_receita, deletar_receita, \
    atualizar_receita
from app.database import get_db
from app.exception.receita_exception import ReceitaException
from app.schemas.receita_schema import DespesaResponse, ReceitaCreate

router = APIRouter()

@router.get("/receitas", response_model=list[DespesaResponse], status_code=200)
def buscar_todas_as_receitas(db:Session = Depends(get_db)):
    return pegar_todas_as_receitas(db=db)


@router.get("/receitas/{receita_id}", response_model=DespesaResponse, status_code=200)
def buscar_receita_por_id(receita_id:int, db:Session=Depends(get_db)):
    try:
        return pegar_receita_por_id(receita_id=receita_id,db=db)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/receitas", response_model=DespesaResponse, status_code=201)
def criar_receita(receita:ReceitaCreate, db:Session= Depends(get_db)):
    try:
        return salvar_receita(db=db,receita=receita)
    except ReceitaException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/receitas/{receita_id}", response_model=DespesaResponse, status_code=200)
def atualizar_receita_crud(receita_id, receita:ReceitaCreate, db:Session= Depends(get_db)):
    try:
        return atualizar_receita(db=db, receita_id=receita_id,receita=receita)
    except ReceitaException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/receitas/{receita_id}", response_model=DespesaResponse, status_code=200)
def excluir_receita(receita_id, db:Session= Depends(get_db)):
    try:
        return deletar_receita(receita_id=receita_id, db=db )
    except NoResultFound as e:
        HTTPException(status_code=404, detail=str(e))
