
from bson.json_util import dumps
import pymongo
import random
import requests


class MongoObject():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["emotions"]
        self.userColl = self.mydb['users']
        self.converColl = self.mydb['conversations']

    def newUser(self,name):
        mydict = {
                "_id": self.maxUserId(),
                "name": name }
        x = self.userColl.insert_one(mydict)
        print(x.inserted_id)
        return x.inserted_id
    
    def getNumUsers(self,qty):
        users_tot = self.userColl.find({})
        dev = random.sample(list(users_tot),int(qty))
        return dumps(dev)

    def maxUserId(self):
        try:
            n = list(self.userColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 0
    
    def newChat(self,nombre,usuarios):
        #args = list(args)
        #formato del array:
        '''{
            "_id": 102,
            "usuarios": [1,2,3]
        }'''
        #print(args)
        mydict = {
                "_id": self.maxChatId(),
                "nombre": nombre,
                "usuarios": [int(a) for a in usuarios],
                "mensajes":[]
                }
        x = self.converColl.insert_one(mydict)
        return x.inserted_id

    def addUser2chat(self,chat_id,idusu):
        # falta verificar:
        #   que el chat existe
        #   que el usuario existe
        #   que no está en el chat
        print(chat_id,idusu)
        x = self.converColl.update({ "_id": int(chat_id) },{ "$push": { "usuarios": int(idusu) } })
        print(x)
        return chat_id
    
    def addMsg2chat(self,chat_id,usuario,mensaje):
        print(chat_id,usuario,mensaje)
        x = self.converColl.update({ "_id": int(chat_id) },{ "$push": { "mensajes": { "autor":int(usuario),"texto":mensaje} } })
        print(x)
        return chat_id

    def maxChatId(self):
        try:
            n = list(self.converColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 1000



#db = MongoObject()

#print(db.maxUserId())
#print(db.newUser('Sergio'))