from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017/")
db = client.SimilarityDB
users = db["users"]

class Register(Resource):
    def post(self):
        req = request.get_json()

        username = req["username"]
        password = req["password"]

        if not validateAuth(req):
            response = {
                "message": "Invalid username/password"
            }
            return make_response(jsonify(response), 301)

        if verifyUsername(username) >= 1:
            response = {
                "message": "User has been existed!"
            }
            return make_response(jsonify(response), 301)

        users.insert({
            "username": username,
            "password": bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()),
            "num_token": 10
        })

        response = {
            "message": "Success!"
        }
        return make_response(jsonify(response), 200)

class Detect(Resource):
    def post(self):
        req = request.get_json()
        
        username = req["username"]
        password = req["password"]
        text_origin = req["text_origin"]
        text_comparison = req["text_comparison"]

        if not validateAuth(req):
            response = {
                "message": "Invalid username/password"
            }
            return make_response(jsonify(response), 301)

        is_verified, hashed_password = verifyPassword(username, password)
        if not is_verified:
            response = {
                "message": "Invalid username/password"
            }
            return make_response(jsonify(response), 302)

        num_token = getToken(username)
        if num_token <= 0:
            response = {
                "message": "Unsufficient token"
            }
            return make_response(jsonify(response), 303)

        substractToken(username, num_token)

        nlp = spacy.load("en_core_web_sm")
        nlp_origin = nlp(text_origin)
        nlp_comparison = nlp(text_comparison)

        ratio = nlp_origin.similarity(nlp_comparison)

        response = {
            "similarity": ratio,
            "message": "Success!"
        }

        return make_response(jsonify(response), 200)
        
class Refill(Resource):
    def post(self):
        req = request.get_json()

        username = req["username"]
        password = req["password"]
        token_refill = req["token_refill"]

        if not validateAuth(req):
            response = {
                "message": "Invalid username/password"
            }
            return make_response(jsonify(response), 301)

        is_verified, hashed_password = verifyPassword(username, password)
        if not is_verified:
            response = {
                "message": "Invalid username/password"
            }
            return make_response(jsonify(response), 302)

        num_token = getToken(username)
        if num_token <= 0:
            response = {
                "message": "Unsufficient token"
            }
            return make_response(jsonify(response), 303)

        current_token = addToken(username, num_token, token_refill)

        response = {
            "message": "Success! Current token: " + current_token
        }

        return make_response(jsonify(response), 200)
        
def validateAuth(request):
    if "username" not in request or "password" not in request:
        return False
    else:
        return True

def verifyUsername(username):
    user_found = users.count_documents({
            "username": request["username"]
        })

    return user_found

def verifyPassword(username, password):
    hashed_password = users.find({
        "username": username
    })[0]["password"]

    if bcrypt.hashpw(password.encode("utf-8"), hashed_password) == hashed_password:
        return True, hashed_password
    else:
        return False, None

def getToken(username):
    return users.find({
        "username": username
    })[0]["num_token"]

def substractToken(username, num_token):
    users.update({
            "username": username
        }, {
            "$set": {"num_token": num_token - 1}
        })

def addToken(username, num_token, refill_amount):
    users.update({
            "username": username
        }, {
            "$set": {"num_token": num_token + refill_amount}
        })
    
    return num_token + refill_amount

api.add_resource(Register, "/register")
api.add_resource(Detect, "/detect")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
    app.run(host="0.0.0.0")