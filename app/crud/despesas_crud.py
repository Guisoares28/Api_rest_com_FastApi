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

def pegar_todas_as_despesas(db:Session):
    return db.query(Despesa).all()

def buscar_despesa_por_id(despesa_id, db:Session):
    return db.query(Despesa).get(despesa_id)

def atualizar_despesa_por_id(despesa_id:int, despesa:DespesaCreate, db:Session):
    despesa_encontrada = db.query(Despesa).get(despesa_id)
    if not despesa_encontrada:
        raise DespesaException("Receita não encontrada")
    despesa_encontrada.descricao = despesa.descricao
    despesa_encontrada.valor = despesa.valor
    despesa_encontrada.data = despesa.data
    despesa_duplicada = db.query(Despesa).filter(and_(
        despesa_id != Despesa.id,
        despesa.descricao == Despesa.descricao,
        despesa.data.month == Extract("month", Despesa.data)
    )).first()
    if despesa_duplicada:
        raise DespesaException("Despesa já cadastrada com está descrição nesse mesmo Mês")
    db.commit()
    db.refresh(despesa_encontrada)
    return despesa_encontrada

def deletar_despesa_por_id(despesa_id:int, db:Session):
    despesa_encontrada = db.query(Despesa).get(despesa_id)
    if not despesa_encontrada:
        raise DespesaException("Despesa não encontrada")
    db.delete(despesa_encontrada)
    db.commit()
    return
