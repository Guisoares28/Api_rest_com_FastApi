from typing import Dict

from pydantic import BaseModel




class Resumo(BaseModel):
    total_receitas_mes: float
    total_despesas_mes: float
    saldo_final: float
    total_por_categoria: Dict[str, float]
