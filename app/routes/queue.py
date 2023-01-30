import json
import uuid
from datetime import datetime

from box import Box
from flask import request
from flask_restx import Resource

from app import api, redis
from app.models.job import queue_job_post

ns = api.namespace('queue', description="Queue operations")


@ns.route('/')
class QueueMain(Resource):
    @ns.doc(description="Gets all jobs on the current queue.")
    def get(self):
        queue = [json.loads(i) for i in reversed(redis.lrange("queue", 0, -1))]
        return {'queue': queue, 'entries': len(queue)}, 200

    @ns.doc(body=queue_job_post, description="Adds a job to the end of the current queue.")
    def post(self):
        u = str(uuid.uuid4())
        d = datetime.utcnow()
        req = Box(request.get_json())
        req.job_id = u
        req.added = d
        redis.lpush("queue", json.dumps(req, default=str))
        return {'id': u}, 200


@ns.route('/all')
class QueueReset(Resource):
    @ns.doc(responses={204: 'No Content'}, description="Deletes all jobs from the queue.")
    def delete(self):
        redis.delete("queue")
        return '', 204
