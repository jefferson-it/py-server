# app.py
from flask import Flask, jsonify, request
from utils.db.db import *


app = Flask(__name__)
Usr = database.collection("users")

@app.route('/', methods=['GET'])
def get_root():
    response = {
        "message": "Hello World!!"
    }
    return jsonify(response)


@app.route('/list_user', methods=['GET'])
def get_list_user():
    limit = int(request.args.get("limit", -1))
    skip = int(request.args.get("skip", 0))

    list_found = Usr.find_many(None, {
        "limit": limit,
        "skip": skip
    }) 
    
    response = list_found

    return jsonify(response)


@app.route("/get_user", methods=['GET'])
def get_a_user():
    name = request.args.get("name")
    response = {}
    exist = Usr.find_one({ "name": name })

    response = {}

    if not exist:
        response["message"] = f"OOPS! User {name} not exist"
    else:
        response["message"] = f"Found!"
        response["data"] = exist

    return jsonify(response)


@app.route('/new_user', methods=['POST'])
def post_new_user():
    body = request.json
    exist = None
    
    if 'name' in body: 
        exist = Usr.find_one({ "name": body["name"] })

    response = {}

    if exist:
        response["message"] = f"Have a user whit name {body["name"]}"
    else:
        result = Usr.insert_one(body)

        if result:
            response["message"] = result['err']
        else:
            response["message"] = f"User saved!"



    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
