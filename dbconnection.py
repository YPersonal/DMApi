#-*- coding: utf-8 -*-

from flask import Flask, jsonify
import flask.ext.restful
from flask.ext.restful import Resource
import redis, re
from pymongo import MongoClient
from settings import MONGO_DB,Mongo_Host,MONGO_PORT,REDIS_URI


class MongodbOption(Resource):
    #初始化
    def __init__(self,*args,**kwargs):
        self.conn = MongoClient(Mongo_Host,MONGO_PORT)
        self.db = self.conn.get_database(MONGO_DB)
        self.redis = redis.StrictRedis.from_url(REDIS_URI)

    @classmethod
    def get_infobyid(self,coll,id):
        try:
            collection = self.db.get_collection(coll)
            result = collection.find_one({"hash_code":id})
        except:
            result = ''
        finally:
            return result

    def get_info(self,coll,page,num):
        list_info = []
        try:
            collection = self.db.get_collection(coll)
            result = collection.find().sort({"publish_date":-1}).skip(page*num).limit(num)

            for item in result:
                list_info.append(item)
        except:
            pass
        finally:
            return list_info

    def delete_one(self,coll,id):
        try:
            collection = self.db.get_collection(coll)
            result = collection.delete_one({"hash_code":id})
            return result.deleted_count
        except:
            return "delete exception,the collection is {}, the hash_code is {}".format(coll,id)

    def update_one(self,coll,id,*args,**kwargs):
        try:
            collection = self.db.get_collection(coll)
            collection.update_one()
        except:
            pass




if __name__ =="__main__":
    # Mongo_Host = 'mongodb://root:123456a!@dds-m5e9988dce6e7ec41.mongodb.rds.aliyuncs.com'
    # MONGO_PORT = 3717
    # MONGO_DB = 'crawler_source'
    # COLLECTION = '新闻资讯'
    # redis_uri = 'redis://:123456789a!@118.190.79.157:6379/0'
    # redis_key = 'industrial_policy'
    n =  MongodbOption()
    n.delete_one(u"新闻资讯",'fb6d084e87464c465a9b147a88715feeca489638')

