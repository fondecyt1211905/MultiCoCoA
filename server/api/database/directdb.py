from pymongo import MongoClient
from bson.objectid import ObjectId
import utils.config as config
conf = config.CONFIG

def connect():
    client = MongoClient(conf["mongo_host"], conf["mongo_port"]) 
    db = client[conf["mongo_db"]]
    return db

def getAnalysis(idAnalysis):
    db = connect()
    analysis = db["analysis"]
    result = list(analysis.aggregate([
        {
            "$match": {
                "_id": ObjectId(idAnalysis)
            }   
        },
        {
            "$lookup": {
                "from": "activity",
                "localField": "id_activity",   
                "foreignField": "_id",
                "as": "activity"
            }
        }   
    ]))[0]
    return result