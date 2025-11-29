from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database

# Função qeu gerencia o ciclo de vida da api para acompanhamentos e testes
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("iniciando api")
    try:
        await database.list_collection_names()
        print("conexão bem sucedida")
    except Exception:
        print(f"falha ao conectar ao banco : {Exception}")
    yield
    print("encerrando api")

# instanciando lifespan no app
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "API rodando", "status": "ok"}