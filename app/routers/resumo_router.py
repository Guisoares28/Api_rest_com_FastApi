from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.resumo_crud import ResumoCrud
from app.database import get_db
from app.depends import token_verifier
from app.schemas.resumo_schema import Resumo

router = APIRouter(dependencies=[Depends(token_verifier)])

@router.get("/resumo/{ano}/{mes}", response_model=Resumo, status_code=200)
def resumo_de_resultados_mes(ano, mes, db:Session = Depends(get_db)):
    rc = ResumoCrud(db=db)
    return rc.resumo(ano=ano, mes=mes)