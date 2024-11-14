from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.despesas_crud import criar_nova_despesa
from app.database import get_db
from app.exception.despesa_exception import DespesaException
from app.schemas.despesa_schema import DespesaCreate
from app.schemas.receita_schema import ReceitaResponse

router = APIRouter()

@router.post("/despesas", response_model=ReceitaResponse, status_code=201)
def criar_despesa(despesa:DespesaCreate, db:Session = Depends(get_db)):
    try:
        return criar_nova_despesa(despesa=despesa, db=db)
    except DespesaException as e:
        raise HTTPException(status_code=400, detail=str(e))