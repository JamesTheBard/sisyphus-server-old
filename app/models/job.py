from app import api
from flask_restx import fields

queue_job_post = api.model('QueueJobPost', {
    'job_title': fields.String(description='The title of the job', required=True),
    'tasks': fields.List(fields.Raw, description='The tasks associated with the job', required=True),
})

queue_job_model = api.model('QueueJobModel', {
    'job_title': fields.String(description='The title of the job'),
    'job_id': fields.String(description='The Job ID for the job'),
    'tasks': fields.List(fields.Raw, description='The tasks associated with the job'),
})

queue_list_model = api.model('QueueJobList', {
    'queue': fields.List(fields.Nested(queue_job_model))
})
