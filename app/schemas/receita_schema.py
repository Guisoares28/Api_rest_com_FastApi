from pydantic import BaseModel
from datetime import date


class ReceitaCreate(BaseModel):
    descricao: str
    valor: float
    data: date


class DespesaResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    data: date

    class Config:
        from_attributes = True