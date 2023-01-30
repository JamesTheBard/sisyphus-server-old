from app import api
from flask_restx import fields


workers_status_model = api.model('WorkerStatusPost', {
    'status': fields.String(description='The current status of the worker.', required=True),
    'hostname': fields.String(description='The hostname of the worker.', required=True),
    'version': fields.String(description='The version of Sisyphus running on the worker.', required=True),
    'task': fields.String(description='The module being run on the worker.'),
    'job_title': fields.String(description='The title of the job being run.'),
    'job_id': fields.String(description='The ID of the job being run.'),
})
