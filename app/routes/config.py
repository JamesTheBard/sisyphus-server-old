import json
import re
import uuid
from datetime import datetime

import humanize
from box import Box
from flask import request
from flask_restx import Resource

from app.version import VERSION
from app.config import Config
from app import api, redis, start_time
from app.models.status import status_model

ns = api.namespace('status', description="Server configuration")


def sanitize_uri(uri):
    regex = r'^(\w+:\/\/\w+:)[^@]+(@(\w|\d|\.)+(?::\d+.+)?)$'
    regex = re.compile(regex)
    if match := regex.search(uri):
        return f'{match.group(1)}********{match.group(2)}'
    return uri


@ns.route('/')
class ServerConfiguration(Resource):
    @ns.marshal_with(status_model)
    def get(self):
        data = Box()
        data.backend = {
            "MONGO_URI": sanitize_uri(Config.MONGO_URI),
            "REDIS_URI": sanitize_uri(Config.REDIS_URI)
        }
        data.version = VERSION
        data.uptime = humanize.naturaldelta(datetime.now() - start_time)
        return data, 200
