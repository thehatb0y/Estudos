import json
from flask import jsonify
from datetime import date

class Customer:
    def __init__(self, cpf, nome, email, dataDeNascimento, sexo, rendaMensal):
        self.id = 0
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.dataDeNascimento = dataDeNascimento
        self.sexo = sexo
        self.rendaMensal = rendaMensal

    def saveCustomer(customer):
        CCustomer = Customer(customer["cpf"], customer["nome"], customer["email"], customer["dataDeNascimento"], customer["sexo"], customer["rendaMensal"])

        with open("/db_jason/customers.json", "r+") as file:
            data = json.load(file)


            for p in data["customers"]:
                if p["cpf"] == CCustomer.cpf:
                    return "CPF já cadastrado!"
            
            CCustomer.id = len(data["customers"]) + 1
            CCustomer = CCustomer.__dict__
            data["customers"].append(CCustomer)

            file.seek(0)
            json.dump(data, file, indent=4)

            for person in data["customers"]:
                if person["id"] == CCustomer["id"]:
                    return jsonify("id: " + str(person["id"]))

        return "Storage Problem"
 
class Product:
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
    
    def saveProduct(product):
        PProduct = Product(product["nome"], product["susep"], product["expiracaoDeVenda"], product["valorMinimoAporteInicial"], product["valorMinimoAporteExtra"], product["idadeDeEntrada"], product["idadeDeSaida"], product["carenciaInicialDeResgate"], product["carenciaEntreResgates"])

        with open("db_json/products.json", "r+") as file:
            data = json.load(file)

            PProduct.id = len(data["products"]) + 1
            PProduct = PProduct.__dict__
            data["products"].append(PProduct)

            file.seek(0)
            json.dump(data, file, indent=4)

            for p in data["products"]:
                if p["id"] == PProduct["id"]:
                    return jsonify("id: " + str(p["id"]))

        return "Storage Problem"

class Plan:
    def __init__(self, customerId, productId, aporte, hiringDate):
        self.id = 0
        self.customerId = customerId
        self.productId = productId
        self.aporte = aporte
        self.hiringDate = hiringDate

    def savePlan(plan):
        PPlan = Plan(plan["customerId"], plan["productId"], plan["aporte"], plan["hiringDate"])
        with open("db_json/plans.json", "r+") as file:
            data = json.load(file)

            PPlan.id = len(data["plans"]) + 1

            #rules

            produto = getItemById(PPlan.productId, "products")
            if produto == False:
                return "Product not found"

            exp = produto["expiracaoDeVenda"]
            delta = date(int(exp[0:4]), int(exp[5:7]), int(exp[8:10])) - date.today()

            if delta.days < 0:
                    return "Product expired"

            customer = getItemById(PPlan.customerId, "customers")
            if customer == False:
                return "Customer not found"

            exp = customer["dataDeNascimento"]
            delta =  (date.today() - date(int(exp[0:4]), int(exp[5:7]), int(exp[8:10])))/365

            if delta.days < produto["idadeDeEntrada"] or delta.days > produto["idadeDeSaida"]:
                return "Customer not allowed"

            if plan["aporte"] < produto["valorMinimoAporteInicial"]:
                return "Aporte not allowed"

            #end rules
            PPlan = PPlan.__dict__
            data["plans"].append(PPlan)

            file.seek(0)
            json.dump(data, file, indent=4)

            for p in data["plans"]:
                if p["id"] == PPlan["id"]:
                    return jsonify("id: " + str(p["id"]))

        return "Storage Problem"

class AporteExtra:
    def __init__(self, customerId, productId, aporte):
        self.id = 0
        self.customerId = customerId
        self.productId = productId
        self.aporte = aporte

    def saveAporteExtra(aporte):
        AAporte = AporteExtra(aporte["customerId"], aporte["productId"], aporte["aporte"])
        with open("db_json/aporteextra.json", "r+") as file:
            data = json.load(file)
            
            AAporte.id = len(data["aporteextra"]) + 1

            #rules
            produto = Product.getProduct(AAporte.productId)
            if AAporte.aporte < produto["valorMinimoAporteExtra"]:
                return "Aporte not allowed"
            #end rules
            
            AAporte = AAporte.__dict__
            data["aporteextra"].append(AAporte)

            file.seek(0)
            json.dump(data, file, indent=4)

            for p in data["aporteextra"]:
                if p["id"] == AAporte["id"]:
                    return jsonify("id: " + str(p["id"]))

        return "Storage Problem"

class Resgate:
    def __init__(self, planId, resgateValue):
        self.id = 0
        self.planId = planId
        self.resgateValue = resgateValue
        self.resgateDate = str(date.today())

    def saveResgate(resgate):
        RResgate = Resgate(resgate["planId"], resgate["resgateValue"])
        aporte = 0 
        data = {}
        with open("db_json/resgates.json", "r+") as file:
            data = json.load(file)

            RResgate.id = len(data["resgates"]) + 1
            #rules
            plano = getItemById(RResgate.planId, "plans")
            if plano == False:
                return "Plan not found"
                
            if plano["aporte"] < RResgate.resgateValue:
                return "Not enough founds"
            aporte = plano["aporte"] - RResgate.resgateValue

            exp = plano["hiringDate"]
            dt = date.today() - date(int(exp[0:4]), int(exp[5:7]), int(exp[8:10]))
            if int(dt.days) < 60:
                return "You need at least 60 days to resgate"

            for p in data["resgates"]:
                dt = date.today() - date(int(p["resgateDate"][0:4]), int(p["resgateDate"][5:7]), int(p["resgateDate"][8:10]))
                if int(dt.days) < 30:
                    return "You need at least 30 days to resgate again"

            #end rules
            RResgate = RResgate.__dict__
            data["resgates"].append(RResgate)

            file.seek(0)
            json.dump(data, file, indent=4)

        with open("db_json/plans.json", "r+") as file2:
            data1 = json.load(file2)
            for p in data1["plans"]:
                if p["id"] == RResgate["planId"]:
                    p["aporte"] = aporte
            file2.seek(0)
            json.dump(data1, file2, indent=4)

        for p in data["resgates"]:
            if p["id"] == len(data["resgates"]):
                return jsonify("id: " + str(p["id"]))

        return "Storage Problem"

# id = id do objeto a ser buscado
# item = nome do arquivo
def getItemById(id, item):
    with open(f"db_json/{item}.json", "r+") as file:
        data = json.load(file)
        for p in data[item]:
            if p["id"] == id:
                return p
        return False