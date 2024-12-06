import os

eventstore_connection_string = os.getenv('EVENT_STORE_CONNECTION_STRING', 'esdb://localhost:2113?tls=false')