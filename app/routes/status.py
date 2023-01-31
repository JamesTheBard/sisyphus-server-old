import re
from datetime import datetime

import humanize
from box import Box
from flask_restx import Resource

from app import api, start_time
from app.config import Config
from app.models.status import status_model
from app.version import VERSION

ns = api.namespace('status', description="Server configuration")


def sanitize_uri(uri):
    regex = r'^(\w+:\/\/\w+:)[^@]+(@(\w|\d|\.)+(?::\d+.+)?)$'
    regex = re.compile(regex)
    if match := regex.search(uri):
        return f'{match.group(1)}********{match.group(2)}'
    return uri


@ns.route('')
class ServerConfiguration(Resource):
    @ns.marshal_with(status_model)
    @ns.doc()
    def get(self):
        data = Box()
        data.backend = {
            "MONGO_URI": sanitize_uri(Config.MONGO_URI),
            "REDIS_URI": sanitize_uri(Config.REDIS_URI)
        }
        data.version = VERSION
        data.uptime = humanize.naturaldelta(datetime.now() - start_time)
        return data, 200
