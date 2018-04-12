#-*- coding: utf-8 -*-

from flask import Flask, jsonify
import flask.ext.restful,json
from flask.ext.restful import Resource
import re, redis, datetime
from pymongo import MongoClient
from settings import MONGO_DB,Mongo_Host,MONGO_PORT,REDIS_URI
from dbconnection import MongodbOption


app = Flask(__name__)
api = flask.ext.restful.Api(app)
conn = MongodbOption()


# def index():
#     return jsonify({"hello":"world"})

@app.route('/find/<string:coll>/<string:id>')
def get_info(coll,id):
    result = conn.db.get_collection(coll).find_one({"hash_code": id},{"_id":0,"create_date":0})

    if result.get("publish_date"):
        publish_date = result.get("publish_date").strftime('%Y-%m-%d %H:%M:%S')
        result.update({"publish_date":publish_date})
    elif result.get("publication_date"):
        publication_date = result.get("publication_date").strftime('%Y-%m-%d %H:%M:%S')
        result.update({"publication_date": publication_date})
    return jsonify({"data":result})

@app.route('/find/<string:coll>')
@app.route('/')
def index():
    return jsonify({"get one":"http://127.0.0.1:5000/find/<sting:collection>/hash_code","get more item":"http://127.0.0.1:5000/find/<sting:collection>/pageNum/pagecount"})




if __name__ == '__main__':
    app.run(debug=True)
