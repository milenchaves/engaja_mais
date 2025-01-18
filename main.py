from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes import organizacao, inscricao, vaga, voluntario

# Configurações de inicialização
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# Inicializa o aplicativo FastAPI
app = FastAPI(lifespan=lifespan)

app.include_router(voluntario.router)
app.include_router(organizacao.router)
app.include_router(vaga.router)
app.include_router(inscricao.router)