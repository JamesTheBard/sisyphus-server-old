from flask_restx import reqparse

worker_data = reqparse.RequestParser(bundle_errors=True)
worker_data.add_argument('module', type=str, required=True)
worker_data.add_argument('dataset', type=str, required=True)
worker_data.add_argument('name', type=str, required=True)

worker_status = reqparse.RequestParser(bundle_errors=True)
worker_status.add_argument('id', type=str, required=True)