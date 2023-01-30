from flask import Flask
from flask_restx import Api, Resource
import redis as r
import pymongo

app = Flask(__name__)
api = Api(app, doc="/doc/")

redis = r.Redis(
    host='10.0.0.117',
)

mongo = pymongo.MongoClient('mongodb://root:root@10.0.0.117:27017')

from app.routes import queue, workers
