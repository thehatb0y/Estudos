import registration
from flask import Flask, request, jsonify
from datetime import date

def main():

    app = Flask(__name__)

    @app.route('/registration/customer', methods=['POST'])
    def registerCustomer():
        user = request.get_json()
        check = registration.Customer.saveCustomer(user)
        if check == False:
            return "CPF já cadastrado!"
        return check

    @app.route('/customer/<int:id>', methods=['GET'])
    def getCustomer(id):
        check = registration.getItemById(id, "customers")
        if check == False:
            return "Cliente não cadastrado!"
        return check

    @app.route('/registration/product', methods=['POST'])
    def registerProduct():
        user = request.get_json()
        check = registration.Product.saveProduct(user)
        if check == False:
            return "SUSEP já cadastrado!"
        return check

    @app.route('/product/<int:id>', methods=['GET'])
    def getProduct(id):
        check = registration.getItemById(id, "products")
        if check == False:
            return "Produto não cadastrado!"
        return check

    @app.route('/registration/plan', methods=['POST'])
    def registerPlan():
        user = request.get_json()
        check = registration.Plan.savePlan(user)
        return check

    @app.route('/plan/<int:id>', methods=['GET'])
    def getPlan(id):
        check = registration.getItemById(id, "plans")
        if check == False:
            return "Plano não cadastrado!"
        return check

    @app.route('/registration/aporte', methods=['POST'])
    def registerAporte():
        user = request.get_json()
        check = registration.AporteExtra.saveAporteExtra(user)
        return check

    @app.route('/aporte/<int:id>', methods=['GET'])
    def getAporteExtra(id):
        check = registration.getItemById(id, "aporteextra")
        if check == False:
            return "Aporte Extra não cadastrado!"
        return check

    @app.route('/registration/resgate', methods=['POST'])
    def registerResgate():
        user = request.get_json()
        check = registration.Resgate.saveResgate(user)
        return check

    @app.route('/resgate/<int:id>', methods=['GET'])
    def getResgate(id):
        check = registration.getItemById(id, "resgates")
        if check == False:
            return "Resgate Extra não cadastrado!"
        return check

    app.run()

if __name__ == '__main__':
    main()