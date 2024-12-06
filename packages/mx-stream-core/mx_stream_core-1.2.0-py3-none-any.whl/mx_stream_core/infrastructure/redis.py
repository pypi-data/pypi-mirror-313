import logging

import redis
import os

from mx_stream_core.config.app import app_name

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_db = os.getenv('REDIS_DB', 0)
redis_password = os.getenv('REDIS_PASSWORD', None)

_r = None

"""
Log the Redis connection details
"""
logging.info(f'[Redis] host: {redis_host}, port: {redis_port}, db: {redis_db}')


def get_redis_client():
    """
    Get a Redis client
    :return:
    """
    global _r
    if _r is None:
        _r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
    return _r


def get_stream_key(stream_name, group):
    """
    Get the key for the stream position
    :param stream_name: event store stream name
    :param group: stream group
    :return:
    """
    return "{}_{}_{}_stream_position".format(app_name, group, stream_name)


def get_stream_position(stream_name, group):
    """
    Get the stream position from Redis
    :param stream_name: event store stream name
    :param group: stream group
    :return:
    """
    key = get_stream_key(stream_name, group)
    stream_position = get_redis_client().get(key)
    return int(stream_position) if stream_position else 0


def set_stream_position(stream_name, group, position):
    """
    Set the stream position in Redis
    :param stream_name:
    :param group:
    :param position:
    :return:
    """
    key = get_stream_key(stream_name, group)
    get_redis_client().set(key, position)
