import logging
import os
from mx_stream_core.infrastructure.redis import get_stream_position
from esdbclient import EventStoreDBClient

"""
Event Store client
"""
_client = None

def get_event_store_client():
    global _client
    if _client is None:
        """
        Event Store connection string
        """
        eventstore_connection_string = os.getenv('EVENT_STORE_CONNECTION_STRING', 'esdb://localhost:2113?tls=false')

        if eventstore_connection_string is None:
            raise ValueError("EVENT_STORE_CONNECTION_STRING is required")
        _client = EventStoreDBClient(eventstore_connection_string)
    return _client

def subscribe_to_stream(stream_name, group):
    """
    Get stream from event store
    :param stream_name: event store stream name
    :param group: event store group name this group will be used to get the stream position key from redis
    :return:
    """
    stream_position = get_stream_position(stream_name, group)
    logging.info(f"[Event Store] subscribe {stream_name} stream from position {stream_position}")

    return get_event_store_client().subscribe_to_stream(
        stream_name=stream_name,
        stream_position=stream_position
    )

def get_stream(stream_name, group, limit=1000):
    """
    Get stream from event store
    :param stream_name: event store stream name
    :param group: event store group name this group will be used to get the stream position key from redis
    :return:
    """
    stream_position = get_stream_position(stream_name, group)
    logging.info(f"[Event Store] get {stream_name} stream from position {stream_position}")

    return get_event_store_client().get_stream(
        stream_name=stream_name,
        stream_position=stream_position + 1,
        limit=limit)
    
