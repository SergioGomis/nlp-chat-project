from flask import Flask, request
from bson.json_util import dumps
from database import MongoObject


app = Flask(__name__)

db = MongoObject()

@app.route('/user/create/<name>')
def newUser(name):
    resul = db.newUser(name)
    return resul, 200

@app.route('/users/rand/<quantity>')
def getRandUsers(quantity):
    dev = db.getRandUsers(quantity)
    return dev

@app.route('/chat/create', methods=['GET'])
def newChat():
    nombre = request.args.get(key='nombre')
    usuarios = request.args.getlist(key='usuarios')

    dev = db.newChat(nombre,usuarios)
    devuel = f'Chat {dev} creado correctamente'
    return devuel, 200

@app.route('/chat/<chat_id>/adduser', methods=['GET'])
def addUser2chat(chat_id):
    usuario = request.args.get(key='usuario')
    x = db.addUser2chat(chat_id,usuario)
    if x == 0:
        dev = "No se ha podido agregar el usuario, revise la información."
    else:
        dev = f'Usuario añadido al chat {x}'
    return dev, 200



@app.route('/chat/<chat_id>/addmessage', methods=['GET'])
def addMsg2chat(chat_id):
    usuario = request.args.get(key='usuario')
    mensaje = request.args.get(key='mensaje')
    x = db.addMsg2chat(chat_id,usuario,mensaje)
    if x == 0:
        dev = "No se ha podido agregar el usuario, revise la información."
    else:
        dev = '✓✓ Mensaje enviado'
        print(f'LOG: Mensaje añadido al chat {x}')
    return dev, 200


@app.route('/chat/<chat_id>/list')
def showChatMsg(chat_id):
    x = db.showChatMsg(chat_id)
    return x, 200

@app.route('/chat/<chat_id>/changename/<nuevonombre>')
def changeChatName(chat_id,nuevonombre):
    db.changeChatName(chat_id,nuevonombre)
    return 'oc', 200

@app.route('/chat/<chat_id>/sentiment')
def getSentiment(chat_id):
    x = db.getSentiment(chat_id)
    return x, 200

@app.route('/user/<user_name>/recommend')
def getRecommendations(user_name):
    x = db.getRecommendations(user_name)
    return x, 200



app.run("0.0.0.0", 5000, debug=True)