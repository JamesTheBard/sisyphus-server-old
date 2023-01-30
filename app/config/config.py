import os

REDIS_URI = os.environ.get('REDIS_URI', 'redis://localhost')
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost')
