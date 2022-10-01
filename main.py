from fastapi import FastAPI
from src.routers import api_router
from fastapi.middleware.cors import CORSMiddleware


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
