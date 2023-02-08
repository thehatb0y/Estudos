from datetime import date, timedelta
import json
from sqlalchemy import create_engine
from flask import Flask, request, jsonify
import pandas as pd
import psycopg2 as pg


class Cliente:
    def __init__(self, cpf, nome, email, dataDeNascimento, sexo, rendaMensal):
        self.id = 0
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.dataDeNascimento = dataDeNascimento
        self.sexo = sexo
        self.rendaMensal = rendaMensal

    def saveCliente(self, connection):
        sql = f"SELECT * FROM public.cliente WHERE cliente_cpf = '{self.cpf}';"
        cursor = connection.cursor()
        cursor.execute(sql, connection)
        #print cursor query
        records = cursor.fetchall()

        if not records:
            sql = "INSERT INTO public.cliente (cliente_id, cliente_cpf, cliente_nome, cliente_email, cliente_dataDeNascimento, cliente_sexo, cliente_rendaMensal) VALUES (DEFAULT,'" + str(self.cpf) + "', '" + self.nome + "', '" + self.email + "', '" + self.dataDeNascimento + "', '" + self.sexo + "', " + str(self.rendaMensal) + ")RETURNING cliente_id"
            cursor.execute(sql)
            records = cursor.fetchall()
            connection.commit()
            cursor.close()
            return jsonify({"id": records[0][0]})
        return False

class Produto:
    def __init__(self, nome, susep, expiracaoDeVenda, valorMinimoAporteInicial, valorMinimoAporteExtra, idadeDeEntrada, idadeDeSaida, carenciaInicialDeResgate, carenciaEntreResgates):
        self.id = 0
        self.nome = nome
        self.susep = susep
        self.expiracaoDeVenda = expiracaoDeVenda
        self.valorMinimoAporteInicial = valorMinimoAporteInicial
        self.valorMinimoAporteExtra = valorMinimoAporteExtra
        self.idadeDeEntrada = idadeDeEntrada
        self.idadeDeSaida = idadeDeSaida
        self.carenciaInicialDeResgate = carenciaInicialDeResgate
        self.carenciaEntreResgates = carenciaEntreResgates

    def saveProduto(self, connection):
        sql = f"SELECT * FROM public.produto WHERE produto_susep = '{self.susep}';"
        cursor = connection.cursor()
        cursor.execute(sql, connection)
        records = cursor.fetchall()

        if not records:
            sql = "INSERT INTO public.produto (produto_id, produto_nome, produto_susep, produto_expiracaoDeVenda, produto_valorMinimoAporteInicial, produto_valorMinimoAporteExtra, produto_idadeDeEntrada, produto_idadeDeSaida, produto_carenciaInicialDeResgate, produto_carenciaEntreResgates) VALUES (DEFAULT,'" + self.nome + "', '" + self.susep + "', '" + self.expiracaoDeVenda + "', " + str(self.valorMinimoAporteInicial) + ", " + str(self.valorMinimoAporteExtra) + ", " + str(self.idadeDeEntrada) + ", " + str(self.idadeDeSaida) + ", " + str(self.carenciaInicialDeResgate) + ", " + str(self.carenciaEntreResgates) + ")RETURNING produto_id"
            cursor.execute(sql)
            records = cursor.fetchall()
            connection.commit()
            cursor.close()
            return jsonify({"id": records[0][0]})
        return False

class Plano:
    def __init__(self, clienteId, productId, aporte, hiringDate):
        self.id = 0
        self.clienteId = clienteId
        self.productId = productId
        self.aporte = aporte
        self.hiringDate = hiringDate

    def savePlano(self, connection):
        cursor = connection.cursor()
        
        ### Verifica Cliente
        sql_plan = f"SELECT * FROM public.cliente WHERE cliente_id = '{self.clienteId}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()

        if not records:
            #print("Cliente não encontrado")
            return False
        delta = (date.today()-(records[0][5]))/365

        ### Verifica Produto
        sql_plan = f"SELECT * FROM public.produto WHERE produto_id = '{self.productId}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()

        if not records:
            #print("Produto não encontrado")
            return False
        
        if date.today() > records[0][3]:
            #print("Data de expiração de venda menor que a data atual")
            return False
        
        if self.aporte < records[0][4]:
            #print("Aporte inicial menor que o valor mínimo")
            return False
        
        if delta.days < records[0][6] or delta.days > records[0][7]:
            #print("Idade do cliente fora do intervalo permitido")
            return False
        
        ### Insere Plano
        sql = "INSERT INTO public.plano (plano_id, produto_id, cliente_id, aporte, datadacontratacao) VALUES (DEFAULT, " + str(self.clienteId) + ", " + str(self.productId) + ", " + str(self.aporte) + ", '" + self.hiringDate + "')RETURNING plano_id"
        cursor.execute(sql)
        records = cursor.fetchall()
        connection.commit()
        cursor.close()
        return jsonify({"id": records[0][0]})

class AporteExtra:
    def __init__(self, clienteId, planoId, aporte):
        self.id = 0
        self.clienteId = clienteId
        self.planoId = planoId
        self.aporte = aporte

    def saveAporteExtra(self, connection):
        cursor = connection.cursor()
        
        ### Verifica Cliente
        sql_plan = f"SELECT * FROM public.cliente WHERE cliente_id = '{self.clienteId}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()

        if not records:
            #print("Cliente não encontrado")
            return False

        ### Verifica Plano
        sql_plan = f"SELECT * FROM public.plano WHERE plano_id = '{self.planoId}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()

        if not records:
            #print("Plano não encontrado")
            return False
        
        ### Verifica Produto
        sql_plan = f"SELECT * FROM public.produto WHERE produto_id = '{records[0][2]}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()

        if not records:
            #print("Produto não encontrado")
            return False
        
        if self.aporte < records[0][6]:
            #print("Aporte extra menor que o valor mínimo")
            return False
        
        if date.today() > records[0][3]:
            #print("Data de expiração de venda menor que a data atual")
            return False
        
        ### Insere Aporte Extra
        sql = "INSERT INTO public.aporteextra (aporteextra_id, plano_id, cliente_id, valoraporte) VALUES (DEFAULT, " + str(self.clienteId) + ", " + str(self.planoId) + ", " + str(self.aporte) + ")RETURNING aporteextra_id"
        cursor.execute(sql)
        records = cursor.fetchall()
        
        connection.commit()
        cursor.close()
        return jsonify({"id": records[0][0]})

class Resgate:
    def __init__(self, planoId, resgateValue):
        self.id = 0
        self.planoId = planoId
        self.resgateValue = resgateValue
        self.resgateDate = str(date.today())

    def saveResgate(self, connection):
        cursor = connection.cursor()
        ### Verifica Plano
        sql_plan = f"SELECT * FROM public.plano WHERE plano_id = '{self.planoId}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()
        aporte_plano = records[0][3]

        if not records:
            print("Plano não encontrado")
            return False

        if aporte_plano < self.resgateValue:
            print("Valor de resgate maior que o valor do plano")
            return False

        ### Verifica Produto
        sql_plan = f"SELECT * FROM public.produto WHERE produto_id = '{records[0][2]}';"
        cursor.execute(sql_plan, connection)
        recordsAux = cursor.fetchall()

        if not recordsAux:
            print("Produto não encontrado")
            return False
        
        crenciaInicialDeResgate = recordsAux[0][8]
        crenciaEntreResgate = recordsAux[0][9]

        if date.today() < records[0][4] + timedelta(days=crenciaInicialDeResgate):
            print("Data de resgate menor que a data de contratação")
            return False

        sql_plan = f"SELECT * FROM public.resgate WHERE plano_id = '{self.planoId}';"
        cursor.execute(sql_plan, connection)
        records = cursor.fetchall()
        
        if records:
            for plan in records:
                if date.today() < plan[3] + timedelta(days=crenciaEntreResgate):
                    print("Data de resgate menor que a data de resgate anterior")
                    return False

        sql_update_query = f"""Update plano set aporte = {aporte_plano - self.resgateValue} where plano_id = '{self.planoId}'"""
        cursor.execute(sql_update_query)

        ### Insere Resgate
        sql = "INSERT INTO public.resgate (resgate_id, plano_id, valorresgate, datadoresgate) VALUES (DEFAULT, " + str(self.planoId) + ", " + str(self.resgateValue) + ", '" + self.resgateDate + "')RETURNING resgate_id"
        cursor.execute(sql)
        records = cursor.fetchall()
        connection.commit()
        cursor.close()
        return jsonify({"id": records[0][0]})

def getItemById(id, item, connection):
    cursor = connection.cursor()
    sql_plan = f"SELECT * FROM public.{item} WHERE {item}_id = '{id}';"
    cursor.execute(sql_plan, connection)
    records = cursor.fetchall()

    if not records:
        return False
    
    return str(records[0])

def main():

    connection = pg.connect(user = "postgres",
                                  password = "zudxwf45",
                                  host = "localhost",
                                  port = "5432",
                                  database = "db_brasilPrev")

    if connection:
        print("Conectado com sucesso!")
    else:
        print("Erro ao conectar!")

    app = Flask(__name__)

    ## GET ##
    @app.route('/cliente/<int:id>', methods=['GET'])
    def getCliente(id):
        check = getItemById(id, "cliente", connection)
        if check == False:
            return "Cliente não encontrado!"
        return check

    @app.route('/produto/<int:id>', methods=['GET'])
    def getProduto(id):
        check = getItemById(id, "produto", connection)
        if check == False:
            return "Produto não encontrado!"
        return check
    
    @app.route('/plano/<int:id>', methods=['GET'])
    def getPlano(id):
        check = getItemById(id, "plano", connection)
        if check == False:
            return "Plano não encontrado!"
        return check

    @app.route('/aporte/<int:id>', methods=['GET'])
    def getAporte(id):
        check = getItemById(id, "aporteextra", connection)
        if check == False:
            return "Aporte não encontrado!"
        return check
    
    @app.route('/resgate/<int:id>', methods=['GET'])
    def getResgate(id):
        check = getItemById(id, "resgate", connection)
        if check == False:
            return "Resgate não encontrado!"
        return check

    ## POST ##
    @app.route('/registrar/cliente', methods=['POST'])
    def setCliente():
        user = request.get_json()
        check = Cliente(user["cpf"], user["nome"], user["email"], user["dataDeNascimento"], user["sexo"], user["rendaMensal"]).saveCliente(connection)
        if check == False:
            return "Problema ao registrar cliente!"
        return check

    @app.route('/registrar/produto', methods=['POST'])
    def setProduto():
        user = request.get_json()
        check = Produto(user["nome"], user["susep"], user["expiracaoDeVenda"], user["valorMinimoAporteInicial"], user["valorMinimoAporteExtra"], user["idadeDeEntrada"], user["idadeDeSaida"], user["carenciaInicialDeResgate"], user["carenciaEntreResgates"]).saveProduto(connection)
        if check == False:
            return "Problema ao registrar produto!"
        return check

    @app.route('/registrar/plano', methods=['POST'])
    def setPlano():
        user = request.get_json()
        check = Plano(user["clienteId"], user["produtoId"], user["aporte"], user["hiringDate"]).savePlano(connection)
        if check == False:
            return "Problema ao registrar plano!"
        return check

    @app.route('/registrar/aporte', methods=['POST'])
    def setAporte():
        user = request.get_json()
        check = AporteExtra(user["clienteId"], user["planoId"], user["aporte"]).saveAporteExtra(connection)
        if check == False:
            return "Problema ao registrar aporte!"
        return check

    @app.route('/registrar/resgate', methods=['POST'])
    def setResgate():
        user = request.get_json()
        check = Resgate(user["planoId"], user["resgateValue"]).saveResgate(connection)
        if check == False:
            return "Problema ao registrar resgate!"
        return check


    app.run()



if __name__ == '__main__':
    main()





#customer = Customer("12345", "Mateus", "mts.c@live.com", "1991-08-19", "M", 3000)
#produto = Produto("Produto 1", "123452", "2021-08-19", 1000, 1000, 18, 70, 0, 0)
#plan = Plano(2, 1, 1200, "2021-08-19")
#aporte = AporteExtra(2, 1, 1000)
#resgate = Resgate(1, 250)

#produto.saveProduto(connection)
#customer.saveCliente(connection)
#plan.savePlano(connection)
#aporte.saveAporteExtra(connection)
#resgate.saveResgate(connection)