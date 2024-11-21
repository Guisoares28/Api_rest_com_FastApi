
from sqlalchemy import Column, Integer, String, Numeric, Date, TIMESTAMP
from sqlalchemy.sql.functions import func

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
    categoria = Column(String, default="outras", nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario = Column(String(20),unique=True, nullable=False)
    senha = Column(String, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())