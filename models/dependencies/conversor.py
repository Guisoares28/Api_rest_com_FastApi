from Dtos.Receita_DTO import ReceitaResponseDto
from models.models import Receita


def converter_receita_para_receita_response(receita: type(Receita)) -> ReceitaResponseDto:
    receita_response = ReceitaResponseDto(
        id=receita.id,
        descricao=receita.descricao,
        valor=receita.valor,
        data=receita.data
    )
    return receita_response
