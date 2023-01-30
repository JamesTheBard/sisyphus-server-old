import os

class Config:
    # Redis and MongoDB URIs
    REDIS_URI = os.environ.get('REDIS_URI', 'redis://localhost')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost')

    # Worker status expiration for Redis
    STATUS_EXPIRY = 10
