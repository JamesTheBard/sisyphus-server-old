from flask_restx import fields

from app import api

backend_model = api.model('BackendModel', {
    'MONGO_URI': fields.String(description='The URI of the MongoDB'),
    'REDIS_URI': fields.String(description='The URI of the Redis server')
})

status_model = api.model('StatusModel', {
    'backend': fields.Nested(backend_model),
    'version': fields.String(description='The version of the server'),
    'uptime': fields.String(description='Current uptime of the server')
})
