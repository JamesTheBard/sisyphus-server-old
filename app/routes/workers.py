import json

from box import Box
from bson import json_util
from flask import make_response, request
from flask_restx import Resource

from app import api, mongo, redis
from app.config import Config
from app.models.workers import workers_progress_model, workers_status_model
from app.parsers.workers import worker_data

ns = api.namespace('worker', description="Worker operations")


@ns.route('/data')
@ns.expect(worker_data)
class WorkersData(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self):
        args = worker_data.parse_args()
        coll = mongo[args["module"]][args["dataset"]]
        record = coll.find_one({"name": args["name"]})
        if not record:
            return None, 404
        return make_response(json_util.dumps(record), 200)

    def post(self):
        args = worker_data.parse_args()
        coll = mongo[args["module"]][args["dataset"]]
        data = request.get_json()
        data['name'] = args['name']
        coll.replace_one({"name": args['name']}, data, upsert=True)
        return data, 200

    @ns.response(204, 'No Content')
    def delete(self):
        args = worker_data.parse_args()
        coll = mongo[args["module"]][args["dataset"]]
        coll.delete_one({"name": args['name']})
        return None, 204


@ns.route('/status')
class WorkersMain(Resource):
    def get(self):
        data = Box()
        for key in redis.keys("worker:*"):
            name = key.decode().split(':')[1]
            data[name] = json.loads(redis.get(key))
            if data[name].status == "in_progress":
                data[name].progress = json.loads(redis.get(f"progress:{name}"))
        return data, 200


@ns.route('/status/<string:worker_id>')
class WorkersStatus(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self, worker_id):
        data = redis.get(f"worker:{worker_id}")
        if not data:
            return {"error": "worker not found"}, 404
        return json.loads(data), 200

    @ns.doc(body=workers_status_model)
    @ns.response(204, 'No Content')
    def post(self, worker_id):
        req = request.get_json()
        redis.set(f"worker:{worker_id}", json.dumps(req), ex=Config.STATUS_EXPIRY)
        return None, 204


@ns.route('/progress')
class WorkersMain(Resource):
    def get(self):
        data = Box()
        for key in redis.keys("progress:*"):
            name = key.decode().split(':')[1]
            data[name] = json.loads(redis.get(key))
        return data, 200


@ns.route('/progress/<string:worker_id>')
class WorkerProgress(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self, worker_id):
        data = redis.get(f"progress:{worker_id}")
        if not data:
            return {"error": "worker not found"}, 404
        return json.loads(data), 200

    @ns.doc(body=workers_progress_model)
    @ns.response(204, 'No Content')
    def post(self, worker_id):
        req = request.get_json()
        redis.set(f"progress:{worker_id}", json.dumps(req), ex=Config.STATUS_EXPIRY)
        return None, 204
