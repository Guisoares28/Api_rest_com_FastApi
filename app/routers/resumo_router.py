from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.resumo_crud import calcular_total_das_receitas_por_mes, resumo
from app.database import get_db
from app.schemas.resumo_schema import Resumo

router = APIRouter()

@router.get("/resumo/{ano}/{mes}", response_model=Resumo, status_code=200)
def resumo_de_resultados_mes(ano, mes, db:Session = Depends(get_db)):
    return resumo(ano=ano, mes=mes, db=db)