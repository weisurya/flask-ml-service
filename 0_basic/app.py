from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/bye')
def bye():
    c = 2 * 12
    s = str(c)
    return s

@app.route('/json')
def json():
    response = {
        'name': 'foo bar',
        'age': 100,
        'phones': [
            { 'tag': 'home', 'number': '12345' }
        ]
    }
    return jsonify(response)

@app.route('/post', methods=["POST"])
def post():
    req = request.get_json()

    if "x" not in req:
        return "ERROR", 305

    x = req["x"]
    y = req["y"]
    z = x+y

    response = {
        "z": z
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True);