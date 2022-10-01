from fastapi import APIRouter

router = APIRouter(tags=['Users'], prefix='/users')

#Teste de rota
@router.get("/")
async def bem_vinda():
    site = "Hello"
    return site.replace('\n', '')
