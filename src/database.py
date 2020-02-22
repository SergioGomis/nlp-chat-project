
from bson.json_util import dumps
from errorHandler import jsonErrorHandler
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pymongo
import random
import requests
import dns
import os
from dotenv import load_dotenv
load_dotenv()


class MongoObject():
    def __init__(self):
        self.myclient = pymongo.MongoClient(os.getenv("MDB_URL"))
        self.mydb = self.myclient["emotions"]
        self.userColl = self.mydb['users']
        self.converColl = self.mydb['conversations']

    @jsonErrorHandler
    def newUser(self,name):
        mydict = {
                "_id": self.maxUserId(),
                "name": name }
        x = self.userColl.insert_one(mydict)
        print(x.inserted_id)
        return x.inserted_id
    
    @jsonErrorHandler
    def getNumUsers(self,qty):
        users_tot = self.userColl.find({})
        dev = random.sample(list(users_tot),int(qty))
        return dumps(dev)

    @jsonErrorHandler
    def maxUserId(self):
        try:
            n = list(self.userColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 0
    
    @jsonErrorHandler
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

    @jsonErrorHandler
    def addUser2chat(self,chat_id,idusu):
        # falta verificar:
        #   que el chat existe
        #   que el usuario existe
        #   que no está en el chat
        print(chat_id,idusu)
        x = self.converColl.update({ "_id": int(chat_id) },{ "$push": { "usuarios": int(idusu) } })
        print(x)
        return chat_id
    
    @jsonErrorHandler
    def addMsg2chat(self,chat_id,usuario,mensaje):
        print(chat_id,usuario,mensaje)
        x = self.converColl.update({ "_id": int(chat_id) },{ "$push": { "mensajes": { "autor":int(usuario),"texto":mensaje} } })
        print(x)
        return chat_id

    @jsonErrorHandler
    def maxChatId(self):
        try:
            n = list(self.converColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 1000

    @jsonErrorHandler
    def showChatMsg(self,chat_id):
        query = self.converColl.find({"_id":int(chat_id)},{"_id":0,"mensajes":1})
        #print(query)
        return query[0]

    @jsonErrorHandler
    def changeChatName(self,chat_id,nuevonombre):
        
        x = self.converColl.update({ "_id": int(chat_id) },{ "$set": { "nombre": nuevonombre } })
        
        return x

    @jsonErrorHandler
    def getSentiment(self,chat_id):
        x = self.converColl.find({"_id":int(chat_id)},{"_id":0,"mensajes":1})
        x = ' '.join(t['texto'] for t in x[0]['mensajes'])
        sia = SentimentIntensityAnalyzer()
        salida = sia.polarity_scores(x)
        return salida