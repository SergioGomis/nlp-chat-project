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
    nombre = request.args.get(key='nombre')
    usuarios = request.args.getlist(key='usuarios')
    x = db.newChat(nombre,usuarios)
    print(f'Chat {x} creado con:')
    for usuario in usuarios:
        print(usuario)
    return 'oc', 200


@app.route('/chat/<chat_id>/adduser', methods=['GET'])
def addUser2chat(chat_id,*args):
    usuario = request.args.get(key='usuario')
    x = db.addUser2chat(chat_id,usuario)
    print(f'usuario añadido al chat {x}')
    return 'oc', 200



@app.route('/chat/<chat_id>/addmessage', methods=['GET'])
def addMsg2chat(chat_id,*args):
    usuario = request.args.get(key='usuario')
    mensaje = request.args.get(key='mensaje')
    x = db.addMsg2chat(chat_id,usuario,mensaje)
    print(f'mensaje añadido al chat {x}')
    return 'oc', 200


app.run("0.0.0.0", 5000, debug=True)