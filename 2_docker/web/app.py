from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def validateRequest(request):
    if "x" not in request or "y" not in request:
        return 301
    else:
        return 200

def validateDivision(request):
    if request["y"] == 0:
        return 302
    else:
        return 200

class Add(Resource):
    def post(self):
        req = request.get_json()
        status_code = validateRequest(req)
        if(status_code != 200):
            response = {
                'Message': "Invalid request data",
                'Status Code': status_code
            }
            return jsonify(response)


        x = req["x"]
        y = req["y"]
        x = int(x)
        y = int(y)
        result = x+y
        response = {
            'Message': result,
            'Status Code': 200
        }
        return jsonify(response)

class Subtract(Resource):
    def post(self):
        req = request.get_json()
        status_code = validateRequest(req)
        if(status_code != 200):
            response = {
                'Message': "Invalid request data",
                'Status Code': status_code
            }
            return jsonify(response)


        x = req["x"]
        y = req["y"]
        x = int(x)
        y = int(y)
        result = x-y
        response = {
            'Message': result,
            'Status Code': 200
        }
        return jsonify(response)

class Divide(Resource):
    def post(self):
        req = request.get_json()
        status_code = validateRequest(req)
        status_code = validateDivision(req)
        if(status_code != 200):
            response = {
                'Message': "Invalid request data",
                'Status Code': status_code
            }
            return jsonify(response)


        x = req["x"]
        y = req["y"]
        x = int(x)
        y = int(y)
        result = x/y
        response = {
            'Message': result,
            'Status Code': 200
        }
        return jsonify(response)

class Multiply(Resource):
    def post(self):
        req = request.get_json()
        status_code = validateRequest(req)
        if(status_code != 200):
            response = {
                'Message': "Invalid request data",
                'Status Code': status_code
            }
            return jsonify(response)


        x = req["x"]
        y = req["y"]
        x = int(x)
        y = int(y)
        result = x*y
        response = {
            'Message': result,
            'Status Code': 200
        }
        return jsonify(response)

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/substract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/division')

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')