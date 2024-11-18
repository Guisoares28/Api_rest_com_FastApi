from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import validator



class Categoria(str, Enum):
    ALIMENTACAO = "alimentação"
    SAUDE = "saude"
    MORADIA = "moradia"
    TRANSPORTE = "transporte"
    EDUCACAO = "educacao"
    LAZER = "lazer"
    IMPREVISTOS = "imprevistos"
    OUTRAS = "outras"


class DespesaCreate(BaseModel):
    descricao:str
    valor:float
    data:date
    categoria: Optional[Categoria] = Field(None)

    @validator("categoria", pre=True, always=True)
    def set_categoria_default(cls, value):
        if not value:
            return Categoria.OUTRAS
        if isinstance(value, str):
            return Categoria(value)
        return value

class DespesaResponse(BaseModel):
    descricao:str
    valor:float
    data:date
    categoria:Categoria
