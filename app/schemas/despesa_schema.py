from datetime import date

from pydantic import BaseModel


class DespesaCreate(BaseModel):
    descricao:str
    valor:float
    data:date

class DespesaResponse(BaseModel):
    descricao:str
    valor:float
    data:date