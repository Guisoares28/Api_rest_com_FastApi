from fastapi import HTTPException


class DespesaException(HTTPException):
    def __init__(self, detail:str):
        super().__init__(status_code=400, detail=detail)