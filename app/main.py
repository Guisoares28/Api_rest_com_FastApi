

from fastapi import FastAPI

from app.database import engine, Base
from app.routers.receita_router import router as receita_router
from app.routers.despesas_router import router as despesa_router

app = FastAPI()

app.include_router(receita_router, tags=["receita"])
app.include_router(despesa_router, tags=["despesa"])
Base.metadata.create_all(bind=engine)

