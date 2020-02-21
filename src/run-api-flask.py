from flask import Flask, request
from bson.json_util import dumps
from database import MongoObject


app = Flask(__name__)

db = MongoObject()

@app.route('/user/create/<name>')
def newUser(name):
    x = db.newUser(name)
    return f'Usuario {name} añadido con id {x}'


@app.route('/users/<quantity>')
def getNumUsers(quantity):
    dev = db.getNumUsers(quantity)
    return dev


@app.route('/chat/create', methods=['GET'])
def newChat(*args):
    usuarios = request.args.getlist(key='usuarios')
    x = db.newChat(usuarios)
    print(f'Chat {x} creado con:')
    for usuario in usuarios:
        print(usuario)
    return 'oc', 200



app.run("0.0.0.0", 5000, debug=True)