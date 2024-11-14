from datetime import datetime

from sqlalchemy import and_, Extract
from sqlalchemy.orm import Session

from app.exception.despesa_exception import DespesaException
from app.models.receita import Despesa
from app.schemas.despesa_schema import DespesaCreate


def criar_nova_despesa(despesa:DespesaCreate, db:Session):
    despesa_existente = db.query(Despesa).filter(and_(
        Despesa.descricao == despesa.descricao,
        Extract("month", Despesa.data) == despesa.data.month
    )).first()
    if despesa_existente:
        raise DespesaException("Despesa já Cadastrada")
    despesa_nova = Despesa(
        descricao = despesa.descricao,
        valor = despesa.valor,
        data = despesa.data
    )
    db.add(despesa_nova)
    db.commit()
    db.refresh(despesa_nova)
    return despesa_nova