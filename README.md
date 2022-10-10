<h1 align="center">:file_cabinet: Projeto Final Luiza < Code > <br>  Grupo 4 - Cosméticos</h1>

<br>

## :memo: Descrição
Aplicação de carrinho de compras, elaborado como projeto final para o LuizaCode.<br>
Para o carrinho de compras deste projeto, foi definido para o negócio de venda a categoria <b>Cosméticos</b>.<br>
A aplicação irá fornecer um conjunto de APIs para um carrinho de compras da categoria definida, sem aplicação de front end.

## :books: Requisitos funcionais

* <b>Cadastro de clientes</b>: Cadastrar um cliente, 
  cadastrar um endereço, pesquisar um cliente, pesquisar um endereço. 
* <b>Gerenciamento de produtos</b>: Cadastrar um produto, atualizar os dados de um produto, pequisar um produto, pesquisar um produto pelo nome, remover um produto.
* <b>Carrinho de compras: 
  * Carrinho de compras aberto</b>: 
    * Adiciona itens ao carrinho, validando se o cliente e o produto adicionado existe.
    * Valida se o cliente já possui um carrinho em aberto. Caso contrário, um novo carrinho é criado.
    * Ao adicionar um item no carrinho, a quantidade de itens e o valor total é atualizado.
    * Altera a quantidade de itens no carrinho. Validando se o produto existe no carrinho, atualizando a quantidade, e o valor total.
    * Consultar carrinho de compras aberto.
  * <b>Carrinho de compras fechado</b>:
    * Fechar o carrinho aberto.



## :wrench: Tecnologias utilizadas
Projeto <b>Python</b>, utilizando o framework <b>FastAPI</b>, com os registros salvos no banco de dados <b>MongoDB</b>, documentado no <b>Swagger<b>.<br>
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

## Bibliotecas do Python no Projeto
<i>inserir</i>

## :rocket: Rodando o projeto
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
## :handshake: Colaboradoras
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/AdavilaGP">
        <img src="https://avatars.githubusercontent.com/u/48567107?v=4" width="100px;" alt="Foto de Adávila no GitHub"/><br>
        <sub>
          <b>Adávila Piristrello</b>
        </sub>
      </a>
    </td>
        <td align="center">
      <a href="https://github.com/CamiSenna">
        <img src="https://avatars.githubusercontent.com/u/112130435?v=4" width="100px;" alt="Foto de Camila Senna no GitHub"/><br>
        <sub>
          <b>Camila Senna</b>
        </sub>
      </a>
    </td>
        <td align="center">
      <a href="https://github.com/FerTarallo">
        <img src="https://avatars.githubusercontent.com/u/84454284?v=4" width="100px;" alt="Foto de Fernanda Tarallo no GitHub"/><br>
        <sub>
          <b>Fernanda Tarallo</b>
        </sub>
      </a>
    </td>
        <td align="center">
      <a href="http://github.com/julianakemi">
        <img src="https://avatars.githubusercontent.com/u/37545707?v=4" width="100px;" alt="Foto de Juliana Akemi no GitHub"/><br>
        <sub>
          <b>Juliana Akemi</b>
        </sub>
      </a>
    </td>
            <td align="center">
      <a href="https://github.com/vanessa-cl">
        <img src="https://avatars.githubusercontent.com/u/83243667?v=4" width="100px;" alt="Foto de Vanessa Lima no GitHub"/><br>
        <sub>
          <b>Vanessa Lima</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## :dart: Status do projeto
Em fase de testes.