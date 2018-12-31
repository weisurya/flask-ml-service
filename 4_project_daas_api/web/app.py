"""
Registration of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve their stored sentence on our database for 1 token

---
Register user   /register   POST    {username, password: string}            200 OK
Store sentence  /sentence   POST    {username, password, sentence: string}  200 OK
                                                                            301 Out of tokens
                                                                            302 Invalid username/password
Retrieve sentence /sentence GET     {username, password: string}            200 OK
                                                                            301 Out of tokens
                                                                            302 Invalid username/password 
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDatabase
users = db["users"]

class Register(Resource):
    def post(self):
        req = request.get_json()

        username = req["username"]
        password = req["password"]

        is_valid = validateAuth(req)
        if not is_valid:
            response = {
                "status": 301,
                "message": "Incorrect username/password"
            }

        hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

        users.insert({
            "username": username,
            "password": hashed_password,
            "sentences": "",
            "num_token": 10
        })

        response = {
            "status": 200,
            "message": "Successfully signed up with username: " + str(username)
        }

        return jsonify(response)

class Sentence(Resource):
    def post(self):
        req = request.get_json()

        username = req["username"]
        password = req["password"]
        sentence = req["sentence"]

        is_valid = validateAuth(req)
        if not is_valid:
            response = {
                "status": 301,
                "message": "Incorrect username/password"
            }

        is_correct = verifyPassword(username, password)
        if not is_correct:
            response = {
                "status": 302,
                "message": "Incorrect username/password"
            }
            return jsonify(response)

        num_token = getToken(username)
        if num_token <= 0:
            response = {
                "status": 301,
                "message": "Unsufficient token"
            }
            return jsonify(response)
        
        users.update({
            "username": username
        }, {
            "$set": {"sentence": sentence, "num_token": num_token - 1}
        })

        response = {
            "status": 200,
            "message": "Sentence updated successfully"
        }
        return jsonify(response)

    def get(self):
        req = request.get_json()

        username = req["username"]
        password = req["password"]
        
        is_valid = validateAuth(req)
        if not is_valid:
            response = {
                "status": 301,
                "message": "Incorrect username/password"
            }

        is_correct = verifyPassword(username, password)
        if not is_correct:
            response = {
                "status": 302,
                "message": "Incorrect username/password"
            }
            return jsonify(response)
        
        num_token = getToken(username)
        if num_token <= 0:
            response = {
                "status": 301,
                "message": "Unsufficient token"
            }
            return jsonify(response)

        sentence = users.find({
            "username": username
        })[0]["sentence"]

        users.update({
            "username": username
        }, {
            "$set": {"sentence": sentence, "num_token": num_token - 1}
        })

        response = {
            "status": 200,
            "sentence": sentence
        }

        return jsonify(response)
        

def validateAuth(request):
    if "username" not in request or "password" not in request:
        return False
    else:
        user_found = users.find({
            "username": request["username"]
        }).count()
        if user_found != 0:
            return False
        else:
            return True

def verifyPassword(username, password):
    hashed_password = users.find({
        "username": username
    })[0]["password"]

    if bcrypt.hashpw(password.encode('utf-8'), hashed_password) == hashed_password:
        return True
    else:
        return False

def getToken(username):
    return users.find({
        "username": username
    })[0]["num_token"]

api.add_resource(Register, '/register')
api.add_resource(Sentence, '/sentence')

if __name__ == "__main__":
    app.run(host='0.0.0.0')