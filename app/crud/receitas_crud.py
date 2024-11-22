from sqlalchemy import and_, Extract
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.exception.receita_exception import ReceitaException
from app.models.classes_modelos import Receita, Despesa
from app.schemas.receita_schema import ReceitaCreate

class ReceitaCrud:
    def __init__(self, db:Session):
        self.db = db

    def pegar_todas_as_receitas(self):
        return self.db.query(Receita).all()

    def pegar_receita_por_id(self,receita_id):
        receita_existente = self.db.query(Receita).get(receita_id)
        if not receita_existente:
            raise NoResultFound("Receita com Id informado não encontrada")
        return receita_existente

    def salvar_receita(self, receita:ReceitaCreate):
        receita_existente = self.db.query(Receita).filter(and_(
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
        self.db.add(new_receita)
        self.db.commit()
        self.db.refresh(new_receita)
        return new_receita

    def atualizar_receita(self, receita_id: int, receita:ReceitaCreate):
        receita_existente = self.db.query(Receita).get(receita_id)
        if not receita_existente:
            raise NoResultFound("Receita com Id informado não encontrada")
        receita_existente.descricao = receita.descricao
        receita_existente.valor = receita.valor
        receita_existente.data = receita.data
        receita_duplicada = self.db.query(Receita).filter(and_(
            receita_existente.id != Receita.id,
            receita_existente.descricao == Receita.descricao,
            receita_existente.data.month == Extract("month",Receita.data)
        )).first()
        if receita_duplicada:
            raise ReceitaException("Receita já cadastrada com essa descrição nesse mês")
        self.db.commit()
        self.db.refresh(receita_existente)
        return receita_existente

    def deletar_receita(self,receita_id:int):
        receita_existente = self.db.query(Receita).get(receita_id)
        if not receita_existente:
            raise NoResultFound("Receita não encontrada")
        self.db.delete(receita_existente)
        self.db.commit()
        return receita_existente

    def buscar_receita_pela_descricao(self,receita_descricao):
        receita_encontrada = self.db.query(Receita).filter_by(descricao=receita_descricao).all()
        if not receita_encontrada:
            raise NoResultFound("Receita não encontrada")
        return receita_encontrada

    def buscar_receita_por_mes(self,receita_ano:int, receita_mes:int):
        receita_encontrada = self.db.query(Receita).filter(
            and_(
         Extract("month", Receita.data) == receita_mes,
         Extract("year", Receita.data) == receita_ano
        )).all()
        return receita_encontrada

