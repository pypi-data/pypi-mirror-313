import random
import time
import json
import logging

from mx_stream_core.infrastructure.event_store import get_stream, subscribe_to_stream
from mx_stream_core.infrastructure.redis import set_stream_position, get_stream_position
from mx_stream_core.infrastructure.spark import spark
from pyspark.sql.types import StructType

from mx_stream_core.utils.telegram import send_telegram_message
from .base import BaseDataSource


class EventStoreDataSource(BaseDataSource):
    def __init__(self, stream_name: str, group_name: str, schema: StructType, chunk_size=5000, max_retries=5, scan_interval_in_seconds=5) -> None:
        self.stream_name = stream_name
        self.group_name = group_name
        self.schema = schema
        self.chunk_size = chunk_size
        self.max_retries = max_retries
        self.scan_interval_in_seconds = scan_interval_in_seconds

    def process_event(self, event_data, func, last_stream_position=0):
        attempt = 0
        while attempt < self.max_retries:
            try:
                streaming_df = spark.createDataFrame(
                    data=event_data,
                    schema=self.schema,
                    verifySchema=False
                )
                func(streaming_df)
                set_stream_position(self.stream_name, self.group_name, last_stream_position)
                # self.__log(f"{len(event_data)} events processed")
                return
            except Exception as e:
                self.__log(f"attempt {attempt + 1} failed with error: {str(e)}")
                attempt += 1
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
                self.__log(f"will try again after {sleep_time:.2f} seconds...")

        self.__log(f"failed to process after {self.max_retries} attempts")
        raise Exception(
            f"{self.__class__.__name__} | {self.stream_name} | failed to process event after {self.max_retries} attempts")

    def batch_process(self, func):
        begin_stream_position = get_stream_position(self.stream_name, self.group_name)
        stream_position = begin_stream_position
        while True:
            events = get_stream(self.stream_name, self.group_name, self.chunk_size)
            event_data = []
            for event in events:
                event_data_payload = json.loads(event.data)
                event_data_payload["type"] = event.type
                event_data.append(event_data_payload)
                stream_position = event.stream_position

            if stream_position <= begin_stream_position:
                break

            self.process_event(event_data, func, stream_position)
            if len(events) < self.chunk_size:
                self.__log(f"End of stream {self.stream_name}")
                break

    def foreach(self, func):
        self.__log(f"Starting...")
        while True:
            self.batch_process(func)
            time.sleep(self.scan_interval_in_seconds)

        # Notice: spark takes time to process event one by one,
        # this will delay the events that come later and the number of delays will increase over time
        # events = subscribe_to_stream(self.stream_name, self.group_name)
        # for event in events:
        #     self.process_event([json.loads(event.data)], func, event.stream_position)

    def __log(self, msg: str):
        common_msg = f"{self.__class__.__name__} | {self.stream_name} | {msg}"
        logging.info(common_msg)
        send_telegram_message(common_msg)
