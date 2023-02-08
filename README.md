# Projeto teste, criação de API e Banco de dados 

O projeto consiste em 2 APIS diferentes, a primeira API foi feita simulando um BD usando arquivos json, a segunda API foi desenvolvida usando o BD projetado com postgreSQL.


Os arquivos main_jsonDB.py e registration.py representam o funcionamento da API com BD simulado com json.

O aqruivo main_postgreSQL.py representa o funcionamento da API utilizando o BD projetado com prostgre.

Todas as regras de negócio apresentadas no desafio foram cumpridas, entretanto haveria ainda muitas outras regras para garantir o funcionamento correto da API em todos os cenários possíveis, evitando retornos indesejados pro usuário ou programador. 

Regras de negócio garantidas:

Customer: 

  * Customers são verificados por CFP, se já houver um usuário cadastrado com o mesmo CPF a API não permitirá um novo registro

Contratação de Planos:

  * Não será possível contratar um produto com prazo de venda expirado.
  * As regras da contratação como valor de aporte, idade mínima de entrada e saída etc., devem ser levadas em consideração.
  * Caso cliente ou produto não forem encontrados, retornará uma mensagem respectiva ao item não achado
  
Aporte Extra:

  * Deve ser validado o valor mínimo de aporte extra do produto.

Resgate:

  * Devem ser validados os prazos de carência para resgate.
  * Deve ser validado o saldo do plano em relação ao valor resgatado.
  * Caso plano não for encontrado, retornará uma mensage
  
## API com postgreSQL: 

###### POST
* /registrar/cliente

<sup> {
    "cpf": 45645092292201,
    "nome": "Jose da Silva",
    "email": "jose@cliente.com",
    "dataDeNascimento": "2010-01-01",
    "sexo": "M",
    "rendaMensal": 2899.5
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Problema ao registrar cliente!": Caso já esteja listado.

* /registrar/produto

<sup> {
    "nome": "Longo Prazo",
    "susep": "15414.900840/2018-1710111",
    "expiracaoDeVenda": "2021-01-01",
    "valorMinimoAporteInicial": 1000,
    "valorMinimoAporteExtra": 100,
    "idadeDeEntrada": 18,
    "idadeDeSaida": 60,
    "carenciaInicialDeResgate": 60,
    "carenciaEntreResgates": 30
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Problema ao registrar produto!": Caso tenha algum problema na alocação do dado.

* /registrar/plano

<sup>{
    "clienteId": 1,
    "pprodutoId": 1,
    "aporte": 250,
    "hiringDate": "2023-01-01"
}</sup>

<sup>Return id: Caso tenha alocado.
 
<sup>Return "Problema ao registrar plano!": Caso tenha algum problema na alocação do dado.

* /registrar/resgate

<sup>{
    "planoId": 1,
    "resgateValue": 300
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Problema ao registrar resgate!": Caso tenha algum problema na alocação do dado.


* /registrar/aporte

<sup>{
    "clienteId": 1,
    "produtoId": 1,
    "aporte": 200,
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Problema ao registrar aporte!": Caso tenha algum problema na alocação do dado.


###### GET
* /cliente/id

<sup>Return Customer or "Cliente não cadastrado!"
<sup></sup>
* /produto/id

<sup>Return Produto or "Produto não cadastrado!"
<sup></sup>
* /plano/id

<sup>Return id or "Plano não cadastrado!"
<sup></sup>
* /resgate/id

<sup>Return Resgate or "Resgate Extra não cadastrado!"
<sup></sup>
* /aporte/id

<sup>Return Aporte or "Aporte Extra não cadastrado!"
<sup></sup>
  
## API com JSON: 

###### POST
* /registration/customer

<sup> {
    "cpf": 45645092292201,
    "nome": "Jose da Silva",
    "email": "jose@cliente.com",
    "dataDeNascimento": "2010-01-01",
    "sexo": "M",
    "rendaMensal": 2899.5
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "CPF já cadastrado!": Caso já esteja listado.

<sup>Return "Storage Problem": Caso tenha algum problema na alocação do dado.


* /registration/product

<sup> {
    "nome": "Longo Prazo",
    "susep": "15414.900840/2018-1710111",
    "expiracaoDeVenda": "2021-01-01",
    "valorMinimoAporteInicial": 1000,
    "valorMinimoAporteExtra": 100,
    "idadeDeEntrada": 18,
    "idadeDeSaida": 60,
    "carenciaInicialDeResgate": 60,
    "carenciaEntreResgates": 30
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Storage Problem": Caso tenha algum problema na alocação do dado.

* /registration/plan

<sup>{
    "customerId": 2,
    "productId": 1,
    "aporte": 1500,
    "hiringDate": "2023-01-01"
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Product not found": Caso produto não seja encontrado.

<sup>Return "Product expired": Caso produto esteja expirado.

<sup>Return "Customer not found": Caso cliente não seja encontrado.

<sup>Return "Customer not allowed": Caso idade do cliente não esteja de acordo.

<sup>Return "Aporte not allowed": Caso aporte seja menor do que o necessário.

<sup>Return "Storage Problem": Caso tenha algum problema na alocação do dado.

* /registration/resgate

<sup>{
    "planId": 1,
    "resgateValue": 300
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "You need at least 30 days to resgate again": Caso o ultimo resgate for em menos de 30 dias 

<sup>Return "You need at least 60 days to resgate": Caso não tenha passado 60 dias desde a compra do plano

<sup>Return "Not enough founds": Caso o plano não tenha fundos

<sup>Return "Plan not found": Caso o plano não for encontrado

<sup>Return "Storage Problem": Caso tenha algum problema na alocação do dado.

* /registration/aporte

<sup>{
    "customerId": 1,
    "productId": 1,
    "aporte": 200,
    "hiringDate": "2023-01-01"
}</sup>

<sup>Return id: Caso tenha alocado.

<sup>Return "Aporte not allowed": Caso aporte seja menor que o minimo

<sup>Return "Storage Problem": Caso tenha algum problema na alocação do dado.


###### GET
* /customer/id

<sup>Return Customer or "Cliente não cadastrado!"
<sup></sup>
* /product/id

<sup>Return Produto or "Produto não cadastrado!"
<sup></sup>
* /plan/id

<sup>Return id or "Plano não cadastrado!"
<sup></sup>
* /resgate/id

<sup>Return Resgate or "Resgate Extra não cadastrado!"
<sup></sup>
* /aporte/id

<sup>Return Aporte or "Aporte Extra não cadastrado!"

 
 ## Bando de Dados: 
Esquema do BD desenvolvido para tarefa.

![alt text](https://user-images.githubusercontent.com/19539499/212508547-fa21f127-d2e2-4a36-808e-757dea2cbbc7.png)
