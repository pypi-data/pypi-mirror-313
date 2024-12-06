import logging
from mx_stream_core.data_sources.base import BaseDataSource
from pyspark.sql import DataFrame
from pyspark.sql.functions import window, col, expr, count


class SparkKafkaAsynchronousDataSource:
    def __init__(self,
                 async_source: BaseDataSource,
                 checkpoint_location=None,
                 watermark_delay_threshold="5 minutes",
                 window_duration="2 minutes",
                 idle_watermark_timeout="5 minutes",
                 ):
        if not async_source:
            raise ValueError("Async data source must be provided")

        self.query = None
        self.async_source = async_source
        self.checkpoint_location = checkpoint_location
        self.watermark_delay_threshold = watermark_delay_threshold
        self.window_duration = window_duration
        self.idle_watermark_timeout = idle_watermark_timeout
        self.window_df = None

    def get(self) -> DataFrame:
        return self.window_df

    def foreach(self, func):
        df = self.async_source.get().withWatermark("timestamp", self.watermark_delay_threshold)
        windowed_df = df.groupBy(
            window(col("timestamp"), self.window_duration),
            col("topic")
        ).agg(
            expr("collect_list(struct(data, kafka_timestamp, timestamp)) as events"),
            count("*").alias("event_count")
        )
        windowed_df = windowed_df.select(
            col("window.start").cast("string").alias("window_start"),
            col("window.end").cast("string").alias("window_end"),
            col("events"),
            col("topic"),
            col("event_count"),
        )
        self.window_df = windowed_df
        self.query = self.window_df.writeStream.option("checkpointLocation", self.checkpoint_location) \
            .outputMode("append") \
            .option("checkpointLocation", self.checkpoint_location) \
            .foreachBatch(lambda batch, epoch_id: self._process_batch(batch, func, epoch_id)).start()

    def _process_batch(self, batch, func, epoch_id):
        try:
            batch_count = batch.count()
            logging.info(f"Processing batch {epoch_id} with {batch_count} records.")
            func(batch, epoch_id)
            logging.info(f"Batch {epoch_id} processed successfully.")
        except Exception as e:
            logging.error(f"Error processing batch {epoch_id}: {e}")
            raise e

    def awaitTermination(self):
        if self.query:
            self.query.awaitTermination()
