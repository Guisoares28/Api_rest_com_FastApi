

from sqlalchemy import Column, Integer, String, Numeric, Date

from app.database import Base


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

