import json

from box import Box
from bson import json_util
from flask import make_response, request
from flask_restx import Resource

from app import api, redis, mongo
from app.models.workers import workers_status_model
from app.parsers.workers import worker_data, worker_status

ns = api.namespace('worker', description="Worker operations")


@ns.route('/')
class WorkersMain(Resource):
    def get(self):
        data = Box()
        for key in redis.keys("worker:*"):
            name = key.decode().split(':')[1]
            data[name] = json.loads(redis.get(key))
            if data[name].status == "in_progress":
                data[name].progress = json.loads(redis.get(f"progress:{name}"))
        return data, 200


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
@ns.expect(worker_status)
class WorkersStatus(Resource):
    @ns.response(200, 'Success')
    @ns.response(404, 'Not Found')
    def get(self):
        args = worker_status.parse_args()
        data = redis.get(f"worker:{args['id']}")
        print(data)
        if not data:
            return {"error": "worker not found"}, 404
        return json.loads(data), 200

    @ns.doc(body=workers_status_model)
    @ns.response(204, 'No Content')
    def post(self):
        args = worker_status.parse_args()
        req = request.get_json()
        redis.set(f"worker:{args['id']}", json.dumps(req))
        return None, 204
