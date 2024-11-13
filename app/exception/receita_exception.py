from fastapi import HTTPException
from pydantic.dataclasses import dataclass


class ReceitaJaCadastrada(HTTPException):
    def __init__(self, detail:str):
        super().__init__(status_code=400, detail=detail)