import json
import uuid
from datetime import datetime

from box import Box
from flask import request
from flask_restx import Resource

from app import api, redis
from app.models.job import queue_job_post, queue_list_model

ns = api.namespace('queue', description="Queue operations")


@ns.route('')
class QueueMain(Resource):
    @ns.doc(description="Gets all jobs on the current queue.")
    @ns.response(200, 'Success', queue_list_model)
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

    @ns.doc(description="Deletes all jobs from the queue.")
    @ns.response(204, 'No Content')
    def delete(self):
        redis.delete("queue")
        return '', 204


@ns.route('/poll')
class QueuePoll(Resource):
    @ns.doc(description="Removes a job from the queue for processing")
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self):
        if job := redis.rpop("queue"):
            return json.loads(job), 200
        return {"message": "there are no jobs on the queue"}, 404
