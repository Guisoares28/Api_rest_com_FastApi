from datetime import datetime

from sqlalchemy import and_, Extract
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.exception.receita_exception import ReceitaException
from app.models.receita import Receita
from app.schemas.receita_schema import ReceitaCreate


def pegar_todas_as_receitas(db:Session):
    return db.query(Receita).all()

def pegar_receita_por_id(db:Session, receita_id):
    receita_existente = db.query(Receita).filter_by(id=receita_id).first()
    if not receita_existente:
        raise NoResultFound("Receita com Id informado não encontrada")
    return receita_existente

def salvar_receita(db:Session, receita:ReceitaCreate):
    receita_existente = db.query(Receita).filter(and_(
        Receita.descricao == receita.descricao,
        Extract("month", Receita.data) == receita.data.month
    )).first()
    if receita_existente:
        raise ReceitaException("Receita já Cadastrada")
    new_receita = Receita(
        descricao = receita.descricao,
        valor = receita.valor,
        data = receita.data
    )
    db.add(new_receita)
    db.commit()
    db.refresh(new_receita)
    return new_receita

def atualizar_receita(db:Session, receita_id: int, receita:ReceitaCreate):
    receita_existente = db.query(Receita).filter_by(id=receita_id).first()
    if not receita_existente:
        raise NoResultFound("Receita com Id informado não encontrada")
    receita_encontrada = (db.query(Receita)
    .filter(and_(Receita.descricao == receita.descricao, Receita.id != receita_id))
    .first()
    )
    if receita_encontrada and datetime.strptime(str(receita_encontrada.data),"%Y-%m-%d").month == receita.data.month:
        raise ReceitaException("Receita já cadastrada com essa descrição neste Mês")

    receita_existente.descricao = receita.descricao
    receita_existente.valor = receita.valor
    receita_existente.data = receita.data
    db.add(receita_existente)
    db.commit()
    db.refresh(receita_existente)
    return receita_existente

def deletar_receita(receita_id:int, db:Session):
    receita_existente = db.query(Receita).filter_by(id=receita_id).first()
    if not receita_existente:
        raise NoResultFound("Receita não encontrada")
    db.delete(receita_existente)
    db.commit()
    return receita_existente

