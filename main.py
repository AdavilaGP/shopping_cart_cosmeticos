import asyncio
from fastapi import FastAPI
from src.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from src.server.database import connect_db, disconnect_db


# criando aplicação
app = FastAPI()
    
# adicionando rotas
app.include_router(api_router)
    
# configurando middleware da aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# evento de conexão e desconexão do banco de dados
app.add_event_handler('startup', connect_db)
app.add_event_handler('shutdown', disconnect_db)
