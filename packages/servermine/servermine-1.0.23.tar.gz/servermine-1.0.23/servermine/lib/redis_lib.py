# redis_connection.py
import redis
import os

redis_client = None
redis_pubsub = None

redis_url = os.getenv('REDIS_URL', None)
redis_user = os.getenv('REDIS_USER', None)
redis_password = os.getenv('REDIS_PASSWORD', None)
redis_host = os.getenv(
    'REDIS_HOST', "redis-10264.c277.us-east-1-3.ec2.redns.redis-cloud.com")
redis_port = os.getenv('REDIS_PORT', "10264")


def set_redis_url(u):
    global redis_url
    redis_url = u


def set_redis_user(u):
    global redis_user
    redis_user = u


def set_redis_password(p):
    global redis_password
    redis_password = p


events = {}

# pool = None
# r = redis.Redis(connection_pool=pool)


def get_url():
    global redis_url, redis_user, redis_password
    if redis_url:
        return redis_url
    elif redis_user and redis_password:
        return f"redis://{redis_user}:{redis_password}@{redis_host}:{redis_port}"


def get_redis_connection():
    global redis_client, redis_url
    if redis_client is None:
        redis_client = redis.from_url(redis_url,
                                      decode_responses=True)
    return redis_client
    # if pool is None:
        # pool = redis.ConnectionPool.from_url(get_url())
    # return redis.Redis(connection_pool=pool, decode_responses=True)

    # if redis_client is None:
    #     if redis_user and redis_password:
    #         redis_url = f"redis://{redis_user}:{redis_password}@redis-10264.c277.us-east-1-3.ec2.redns.redis-cloud.com:10264"
    #     redis_client = redis.from_url(redis_url,
    #                                   decode_responses=True)
    #     # redis_client = redis.Redis(
    #     #     host='localhost', port=6379, decode_responses=True)


def get_redis_pubsub():
    global redis_pubsub
    if redis_pubsub is None:
        redis_pubsub = get_redis_connection().pubsub()
        redis_pubsub.run_in_thread(sleep_time=0.001)
    return redis_pubsub
