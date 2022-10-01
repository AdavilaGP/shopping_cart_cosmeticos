# shopping_cart_cosmeticos
Carrinho de compras para produtos cosméticos elaborado como projeto final para o LuizaCode

# Rodando a aplicação
Após fazer o clone do projeto, é necessário fazer a instalação dos requerimentos da aplicação dentro de um ambiente virtual no terminal:
```
pip install -r requirements.txt
```
Em seguida, basta executar a aplicação em um servidor local utilizado o comando abaixo no terminal: 
```
uvicorn main:app --reload
```
Após abrir o servidor local no navegador basta acessar a rota users na URL para ver a aplicação funcionando.
```
http://127.0.0.1:8000/users/
```
