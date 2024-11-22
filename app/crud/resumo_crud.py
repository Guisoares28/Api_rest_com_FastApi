from operator import and_

from sqlalchemy import Extract, func
from sqlalchemy.orm import Session

from app.models.classes_modelos import Receita, Despesa
from app.schemas.resumo_schema import Resumo


class ResumoCrud:
    def __init__(self, db:Session):
        self.db = db

    def calcular_total_das_receitas_por_mes(self, ano, mes):
        receitas = self.db.query(Receita).filter(
            and_(
                Extract("year", Receita.data) == ano,
                Extract("month", Receita.data) == mes
            )
        ).all()
        return sum(receita.valor for receita in receitas)

    def calcular_total_das_despesas_por_mes(self, ano, mes):
        despesas = self.db.query(Despesa).filter(
            and_(
                Extract("year", Despesa.data) == ano,
                Extract("month", Despesa.data) == mes
            )
        ).all()
        return sum(despesa.valor for despesa in despesas)


    def saldo_final_do_mes(self, total_receita, total_despesa):
        total_mes = total_receita - total_despesa
        return total_mes

    def valor_total_gasto_por_categoria(self):
        resultados = (
            self.db.query(Despesa.categoria, func.sum(Despesa.valor).label("total"))
            .group_by(Despesa.categoria)
            .all()
        )
        return {categoria: total for categoria, total in resultados}


    def resumo(self, ano, mes):
        total_receita_mes = self.calcular_total_das_receitas_por_mes(ano=ano, mes=mes)
        total_despesa_mes = self.calcular_total_das_despesas_por_mes(ano=ano, mes=mes)
        saldo_final = self.saldo_final_do_mes(total_receita_mes, total_despesa_mes)
        valor_categoria = self.valor_total_gasto_por_categoria()
        resumo = Resumo(
            total_receitas_mes= total_receita_mes,
            total_despesas_mes= total_despesa_mes,
            saldo_final= saldo_final,
            total_por_categoria=valor_categoria
        )
        return resumo