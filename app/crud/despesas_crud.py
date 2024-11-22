from sqlalchemy import and_, Extract
from sqlalchemy.orm import Session

from app.exception.despesa_exception import DespesaException
from app.models.classes_modelos import Despesa
from app.schemas.despesa_schema import DespesaCreate

class DespesaCrud:
    def __init__(self, db: Session):
        self.db = db

    def criar_nova_despesa(self, despesa:DespesaCreate):
        despesa_existente = self.db.query(Despesa).filter(and_(
            Despesa.descricao == despesa.descricao,
            Extract("month", Despesa.data) == despesa.data.month
        )).first()
        if despesa_existente:
            raise DespesaException("Despesa já Cadastrada")
        despesa_nova = Despesa(
            descricao = despesa.descricao,
            valor = despesa.valor,
            data = despesa.data,
            categoria = despesa.categoria
        )
        self.db.add(despesa_nova)
        self.db.commit()
        self.db.refresh(despesa_nova)
        return despesa_nova

    def pegar_todas_as_despesas(self):
        return self.db.query(Despesa).all()

    def buscar_despesa_por_id(self,despesa_id):
        return self.db.query(Despesa).get(despesa_id)

    def atualizar_despesa_por_id(self,despesa_id:int, despesa:DespesaCreate):
        despesa_encontrada = self.db.query(Despesa).get(despesa_id)
        if not despesa_encontrada:
            raise DespesaException("Receita não encontrada")
        despesa_encontrada.descricao = despesa.descricao
        despesa_encontrada.valor = despesa.valor
        despesa_encontrada.data = despesa.data
        despesa_duplicada = self.db.query(Despesa).filter(and_(
            despesa_id != Despesa.id,
            despesa.descricao == Despesa.descricao,
            despesa.data.month == Extract("month", Despesa.data)
        )).first()
        if despesa_duplicada:
            raise DespesaException("Despesa já cadastrada com está descrição nesse mesmo Mês")
        self.db.commit()
        self.db.refresh(despesa_encontrada)
        return despesa_encontrada

    def deletar_despesa_por_id(self,despesa_id:int):
        despesa_encontrada = self.db.query(Despesa).get(despesa_id)
        if not despesa_encontrada:
            raise DespesaException("Despesa não encontrada")
        self.db.delete(despesa_encontrada)
        self.db.commit()
        return

    def buscar_despesa_por_descricao(self,despesa_descricao: str):
        despesa_encontrada = self.db.query(Despesa).filter_by(descricao=despesa_descricao).all()
        if not despesa_encontrada:
            raise DespesaException("Despesa não encontrada")
        return despesa_encontrada

    def buscar_despesa_por_mes(self,mes:int, ano:int):
        despesas_encontradas = self.db.query(Despesa).filter(
            and_(
                Extract("year", Despesa.data) == ano,
                Extract("month", Despesa.data) == mes
            )
        ).all()
        return despesas_encontradas