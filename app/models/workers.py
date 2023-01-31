from flask_restx import fields

from app import api

workers_status_model = api.model('WorkerStatusPost', {
    'status': fields.String(description='The current status of the worker.', required=True),
    'hostname': fields.String(description='The hostname of the worker.', required=True),
    'version': fields.String(description='The version of Sisyphus running on the worker.', required=True),
    'task': fields.String(description='The module being run on the worker.'),
    'job_title': fields.String(description='The title of the job being run.'),
    'job_id': fields.String(description='The ID of the job being run.'),
})

workers_progress_model = api.model('WorkerProgressPost', {
    'current_frame': fields.Integer(description='The current frame being processed'),
    'total_frames': fields.Integer(description='The total number of frames')
})