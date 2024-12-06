import os

default_kafka_bootstrap_server = os.getenv('KAFKA_HOST', 'kafka:9092')
