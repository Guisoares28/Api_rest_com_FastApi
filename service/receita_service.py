from typing import List, Union

from fastapi import HTTPException

from dto.receita_dto import ReceitaResponseDto, ReceitaRequestDto
from models.dependencies.dependencies import  get_db
from models.models import Receita
from sqlalchemy.orm import Session


db = Session(get_db())


def salvar_receita_no_banco_de_dados(receita:ReceitaRequestDto) -> ReceitaResponseDto:
    receita_encontrada = buscar_receita_por_descricao(receita.descricao)
    if receita_encontrada:
        receita_response = converter_receita_para_receita_response(receita_encontrada)
        if receita_response.data.month == receita.data.month:
            raise HTTPException(status_code=400, detail="Já existe uma receita criada com está descrição.")
    nova_receita = Receita(
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data
    )
    db.add(nova_receita)
    db.commit()
    db.refresh(nova_receita)

    return converter_receita_para_receita_response(nova_receita)


#Está função converte uma instancia de Receita para ReceitaResponseDto
def converter_receita_para_receita_response(receita: type(Receita)) -> ReceitaResponseDto:
    receita_response = ReceitaResponseDto(
        id=receita.id,
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data
    )
    return receita_response


#Está função tenta encontrar uma receita por Id, caso não for encontrado retorna None
def buscar_receita_por_id(id_receita:int) -> Union[type(ReceitaResponseDto), None]:
    receita_encontrada = db.query(Receita).filter_by(id=id_receita).first()
    if receita_encontrada:
        return converter_receita_para_receita_response(receita_encontrada)
    else:
        return None


#Está função tenta encontrar uma receita por descricao, caso não for encontrado retorna None
def buscar_receita_por_descricao(descricao) -> Union[type(Receita), None]:
    receita_encontrada = db.query(Receita).filter_by(descricao=descricao).first()
    if receita_encontrada:
        return receita_encontrada
    else:
        return None

def converter_lista_de_receitas_para_lista_de_responsedto(receitas: List[type(Receita)]) -> List[ReceitaResponseDto]:
    receitas_response_dto = []
    for receita in receitas:
        receitas_response_dto.append(receita)
    return receitas_response_dto


def buscar_todas_as_receitas_do_banco() -> List[ReceitaResponseDto]:
    receitas = db.query(Receita).all()
    return converter_lista_de_receitas_para_lista_de_responsedto(receitas)




