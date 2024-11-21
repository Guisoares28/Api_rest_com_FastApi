from operator import and_

from sqlalchemy import Extract, func
from sqlalchemy.orm import Session

from app.models.classes_modelos import Receita, Despesa
from app.schemas.resumo_schema import Resumo


def calcular_total_das_receitas_por_mes(ano, mes, db:Session):
    receitas = db.query(Receita).filter(
        and_(
            Extract("year", Receita.data) == ano,
            Extract("month", Receita.data) == mes
        )
    ).all()
    return sum(receita.valor for receita in receitas)

def calcular_total_das_despesas_por_mes(ano, mes, db:Session):
    despesas = db.query(Despesa).filter(
        and_(
            Extract("year", Despesa.data) == ano,
            Extract("month", Despesa.data) == mes
        )
    ).all()
    return sum(despesa.valor for despesa in despesas)

def saldo_final_do_mes(total_receita, total_despesa):
    total_mes = total_receita - total_despesa
    return total_mes

def valor_total_gasto_por_categoria(db:Session):
    resultados = (
        db.query(Despesa.categoria, func.sum(Despesa.valor).label("total"))
        .group_by(Despesa.categoria)
        .all()
    )
    return {categoria: total for categoria, total in resultados}


def resumo(ano, mes, db:Session):
    total_receita_mes = calcular_total_das_receitas_por_mes(ano=ano, mes=mes, db=db)
    total_despesa_mes = calcular_total_das_despesas_por_mes(ano=ano, mes=mes, db=db)
    saldo_final = saldo_final_do_mes(total_receita_mes, total_despesa_mes)
    valor_categoria = valor_total_gasto_por_categoria(db=db)
    resumo = Resumo(
        total_receitas_mes= total_receita_mes,
        total_despesas_mes= total_despesa_mes,
        saldo_final= saldo_final,
        total_por_categoria=valor_categoria
    )
    return resumo