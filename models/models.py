
from sqlalchemy import Column, Integer, Numeric, String, Date
from models.dependencies.dependencies import Base
#Cria a base do modelo


#Define o modelo receitas
class Receita(Base):
    __tablename__ = 'receitas'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    descricao = Column(String, nullable=False)  
    valor = Column(Numeric, nullable=False)
    data = Column(Date, nullable=False)


#Define o modelo despesas
class Despesa(Base):
    __tablename__ = 'despesas'
    id = Column(Integer, primary_key=True, index=True) 
    descricao = Column(String, nullable=False)  
    valor = Column(Numeric, nullable=False)
    data = Column(Date, nullable=False)
    