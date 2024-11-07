from pydantic import BaseModel
from datetime import date

class ReceitaRequestDto(BaseModel):
    descricao: str
    valor: float
    data: date

    class Config:
        arbitrary_types_allowed = True

class ReceitaResponseDto(BaseModel):
    id: int
    descricao: str
    valor: float
    data: date

    class Config:
        arbitrary_types_allowed = True