from pyspark.sql import DataFrame

from mx_stream_core.infrastructure.kafka import produce_kafka_messages

from .base import BaseDataSink


class KafkaDataSink(BaseDataSink):
    def __init__(self, topic, event_name) -> None:
        self.topic = topic
        self.event_name = event_name

    def put(self, df: DataFrame) -> None:
        produce_kafka_messages(
            topic=self.topic,
            df=df,
            event_name=self.event_name
        )
