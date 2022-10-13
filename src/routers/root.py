from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return 'Seja bem vindo! Para visualizar todas as rotas favor acessar /docs'
