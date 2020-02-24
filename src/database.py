from bson.json_util import dumps
from errorHandler import jsonErrorHandler
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as distance
import pymongo
import random
import requests
import pandas as pd
import numpy as np
import dns

from config import dbURL

client = pymongo.MongoClient(dbURL)
print(f"Connecting to {dbURL}")

nltk.download('vader_lexicon')



class MongoObject():
    def __init__(self):
        #self.myclient = client.get_default_database()["emotions"]
        self.mydb = client.get_default_database()
        self.userColl = self.mydb['users']
        self.converColl = self.mydb['conversations']

    @jsonErrorHandler
    def newUser(self,name):
        mydict = {
                "_id": self.maxUserId(),
                "name": name }
        if not self.userColl.find_one({'name':name}):
            x = self.userColl.insert_one(mydict)
            return f'Usuario {name} añadido con id {x.inserted_id}'
        else:
            return 'El usuario ya existe'

    @jsonErrorHandler
    def getRandUsers(self,qty):
        users_tot = self.userColl.find({})
        dev = random.sample(list(users_tot),int(qty))
        return dumps(dev)

    @jsonErrorHandler
    def maxUserId(self):
        try:
            n = list(self.userColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 1
    
    @jsonErrorHandler
    def getUserByName(self,name):
        print('LOG: Buscando a',name)
        dev = self.userColl.find_one({"name":name})
        return dev

    @jsonErrorHandler
    def getNameById(self,userId):
        print('LOG: Buscando id',userId)
        dev = self.userColl.find_one({"_id":userId})
        return dev

    @jsonErrorHandler
    def newChat(self,nombre,usuarios):
        idusuarios = [self.getUserByName(usu) for usu in usuarios]
        mydict = {
                "_id": self.maxChatId(),
                "nombre": nombre,
                "usuarios": [int(a['_id']) for a in idusuarios],
                "mensajes":[]
                }
        dev = self.converColl.insert_one(mydict)
        return dev.inserted_id

    @jsonErrorHandler
    def chatExists(self,chat_id):
        print('LOG: Buscando chat',chat_id)
        dev = self.converColl.find_one({"_id":int(chat_id)})
        if not dev:
            print("LOG: no existe")
            return 0
        return dev

    @jsonErrorHandler
    def addUser2chat(self,chat_id,usuario):
        print('LOG:',chat_id,usuario)
        if self.chatExists(chat_id) != 0:
            idUsu = self.getUserByName(usuario)
            if idUsu:
                x = self.converColl.update({ "_id": int(chat_id) },{ "$push": { "usuarios": int(idUsu['_id']) } })
                if x:
                    return chat_id
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    @jsonErrorHandler
    def userInChat(self,chat_id,idusu):
        print('LOG: Buscando usuario en el chat',chat_id)
        dev = self.converColl.find_one({"_id":int(chat_id),"usuarios":int(idusu)})
        if not dev:
            print("LOG: no existe")
            return 0
        return dev

    @jsonErrorHandler
    def addMsg2chat(self,chat_id,usuario,mensaje):
        print('LOG:',chat_id,usuario,mensaje)
        if self.chatExists(chat_id) != 0:
            idUsu = self.getUserByName(usuario)
            if idUsu:
                if self.userInChat(chat_id,idUsu["_id"]) != 0:
                    x = self.converColl.update({ "_id": int(chat_id) },{ "$push": { "mensajes": { "autor":idUsu["_id"],"texto":mensaje} } })
                    if x:
                        return chat_id
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    @jsonErrorHandler
    def maxChatId(self):
        try:
            n = list(self.converColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 1001

    @jsonErrorHandler
    def showChatMsg(self,chat_id):
        query = self.converColl.find({"_id":int(chat_id)},{"_id":0,"mensajes":1})
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


    @jsonErrorHandler
    def getRecommendations(self,usu_recom):
        x = self.converColl.find({},{"_id":0,"mensajes":1})
        usuarios = []
        mensajes = []
        for elem in x:
            for e in elem['mensajes']:
                usuarios.append(e['autor'])
                mensajes.append(e['texto'])
        df = pd.DataFrame({"usuarios":usuarios,"mensajes":mensajes})
        df = pd.DataFrame(df.groupby("usuarios")["mensajes"].apply(list))
        df['mensajes'] = df['mensajes'].apply(lambda texto: " ".join(texto))
        df=df.reset_index()
        data = { a:b for a,b in zip(list(df['usuarios']),list(df['mensajes']))}
        count_vectorizer = CountVectorizer()
        sparse_matrix = count_vectorizer.fit_transform(data.values())
        doc_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=data.keys())
        similarity_matrix = distance(df,df)
        sim_df = pd.DataFrame(similarity_matrix, columns=data.keys(), index=data.keys())
        np.fill_diagonal(sim_df.values, 0)
        recomendados_df = sim_df[int(self.getUserByName(usu_recom)['_id'])].sort_values(ascending=False).head(3)
        list_ids = list(recomendados_df.index)
        list_values = list(recomendados_df.values)
        list_names = [self.getNameById(usu)['name'] for usu in list_ids]
        print(list_names)
        dev = {a:round(b,3) for a,b in zip(list_names,list_values)}
        print(dev)
        return dev