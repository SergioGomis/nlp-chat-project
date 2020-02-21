
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
    
    def newChat(self,*args):
        args = list(args)

        '''{
            "_id": 102,
            "usuarios": [1,2,3]
        }'''
        print(args)
        mydict = {
                "_id": self.maxChatId(),
                "usuarios": [int(a) for a in args[0]]
                }
        x = self.converColl.insert_one(mydict)
        return x.inserted_id

    def maxChatId(self):
        try:
            n = list(self.converColl.find({},{"_id":1}).sort([('_id', -1)]).limit(1))[0]['_id']
            return n + 1
        except:
            return 1000



#db = MongoObject()

#print(db.maxUserId())
#print(db.newUser('Sergio'))