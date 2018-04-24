#coding: utf-8
import pymongo

def get_db_connection():
    mongo_connect = pymongo.MongoClient("127.0.0.1", port=27017)
    db = mongo_connect["quantTradeSystemDB"]
    return db