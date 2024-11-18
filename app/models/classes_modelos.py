

from sqlalchemy import Column, Integer, String, Numeric, Date, Enum

from app.database import Base
from app.schemas.despesa_schema import Categoria


class Receita(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)
    valor = Column(Numeric(10,2), nullable=False)
    data = Column(Date, nullable=False)


class Despesa(Base):

    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)
    valor = Column(Numeric(10,2), nullable=False)
    data = Column(Date, nullable=False)
    categoria = Column(String, default="outras", nullable=False)


