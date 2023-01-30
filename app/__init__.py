from flask import Flask
from flask_restx import Api, Resource
from datetime import datetime
from app.config import config
import redis as r
import pymongo

app = Flask(__name__)
api = Api(app, doc="/doc/")

redis = r.from_url(config.REDIS_URI)
mongo = pymongo.MongoClient(config.MONGO_URI)

start_time = datetime.now()

from app.routes import queue, workers, config
