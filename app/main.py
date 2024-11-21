from ctypes.wintypes import tagSIZE

from fastapi import FastAPI

from app.database import engine, Base
from app.routers.resumo_router import router as resumo_router
from app.routers.receita_router import router as receita_router
from app.routers.despesas_router import router as despesa_router
from app.routers.user_route import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(receita_router, tags=["receita"])
app.include_router(despesa_router, tags=["despesa"])
app.include_router(resumo_router, tags=["resumo"])
app.include_router(user_router, tags=["user"])



