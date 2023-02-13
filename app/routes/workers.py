import json

from box import Box
from bson import json_util
from flask import make_response, request
from flask_restx import Resource

from app import api, mongo, redis
from app.config import Config
from app.models.workers import (workers_data_model, workers_progress_model,
                                workers_status_model)
from app.parsers.workers import worker_data

ns = api.namespace('worker', description="Worker operations")


@ns.route('/data')
@ns.expect(worker_data)
class WorkersData(Resource):
    @ns.doc(description="Get module-specific data from the datastore")
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self):
        args = worker_data.parse_args()
        module = Config.DATA_PREFIX + args["module"]
        coll = mongo[module][args["dataset"]]
        record = coll.find_one({"name": args["name"]})
        if not record:
            return None, 404
        return make_response(json_util.dumps(record), 200)

    @ns.doc(description="Push module-specific data to the datastore")
    @ns.expect(workers_data_model)
    def post(self):
        args = worker_data.parse_args()
        module = Config.DATA_PREFIX + args["module"]
        coll = mongo[module][args["dataset"]]
        data = request.get_json()
        data['name'] = args['name']
        coll.replace_one({"name": args['name']}, data, upsert=True)
        return data, 200

    @ns.doc(description="Delete module-specific data in the datastore")
    @ns.response(204, 'No Content')
    def delete(self):
        args = worker_data.parse_args()
        module = Config.DATA_PREFIX + args["module"]
        coll = mongo[module][args["dataset"]]
        coll.delete_one({"name": args['name']})
        return None, 204


@ns.route('/status')
class WorkersMain(Resource):
    @ns.doc(description="Get the status of all encoder clients")
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
    @ns.doc(description="Get the status of a specific worker by ID")
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self, worker_id):
        data = redis.get(f"worker:{worker_id}")
        if not data:
            return {"error": "worker not found"}, 404
        return json.loads(data), 200

    @ns.doc(body=workers_status_model, description="Push the status of a specific worker by ID")
    @ns.response(204, 'No Content')
    def post(self, worker_id):
        req = request.get_json()
        redis.set(f"worker:{worker_id}", json.dumps(
            req), ex=Config.STATUS_EXPIRY)
        return None, 204


@ns.route('/progress')
class WorkersMain(Resource):
    @ns.doc(description="Get the progress of all workers")
    def get(self):
        data = Box()
        for key in redis.keys("progress:*"):
            name = key.decode().split(':')[1]
            data[name] = json.loads(redis.get(key))
        return data, 200


@ns.route('/progress/<string:worker_id>')
class WorkerProgress(Resource):
    @ns.doc(description="Get the progress of a worker by ID")
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self, worker_id):
        data = redis.get(f"progress:{worker_id}")
        if not data:
            return {"error": "worker not found"}, 404
        return json.loads(data), 200

    @ns.doc(body=workers_progress_model, description="Push the current progress of a worker via ID")
    @ns.response(204, 'No Content')
    def post(self, worker_id):
        req = request.get_json()
        redis.set(f"progress:{worker_id}", json.dumps(
            req), ex=Config.STATUS_EXPIRY)
        return None, 204


@ns.route('/disable/<string:worker_id>')
@ns.response(200, 'Success')
@ns.response(404, 'Not Found')
class WorkerDisable(Resource):
    @ns.doc(description="Get disable status of a worker by ID")
    def get(self, worker_id):
        if not redis.get(f'worker:{worker_id}'):
            return {"message": "worker not found"}, 404
        if not (r := redis.get(f'server:{worker_id}')):
            return {"disabled": False}, 200
        data = json.loads(r)
        return {"disabled": data.get("disabled", False)}

    @ns.doc(description="Disable a worker by ID")
    def post(self, worker_id):
        if not redis.get(f'worker:{worker_id}'):
            return {"message": "worker not found"}, 404
        if not (r := redis.get(f'server:{worker_id}')):
            data = {"disabled": True}
            redis.set(f'server:{worker_id}', json.dumps(data))
            return data, 200
        data = json.loads(r)
        data['disabled'] = True
        redis.set(f'server:{worker_id}', json.dumps(data))
        return {"disabled": True}

    @ns.doc(description="Clear disabled status on worker by ID")
    def delete(self, worker_id):
        if not redis.get(f'worker:{worker_id}'):
            return {"message": "worker not found"}, 404
        if not (r := redis.get(f'server:{worker_id}')):
            return {"disabled": False}
        data = r.loads(r)
        if data.get('disabled'):
            data['disabled'] = False
            redis.set(f'server:{worker_id}', data)
        return {"disabled": False}
