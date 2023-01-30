from app import api
from flask_restx import fields

queue_job_post = api.model('QueueJobPost', {
    'job_title': fields.String(description='The title of the job', required=True),
    'tasks': fields.List(fields.Raw, description='The tasks associated with the job', required=True),
})
