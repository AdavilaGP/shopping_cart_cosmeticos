from fastapi import FastAPI


app = FastAPI()

#Teste de rota
@app.get("/")
async def bem_vinda():
    site = "Hello"
    return site.replace('\n', '')
