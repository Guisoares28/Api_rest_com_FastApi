from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    usuario:str
    senha:str


class UserResponse(BaseModel):
    id:int
    usuario:str
    senha:str
    criado_em:datetime