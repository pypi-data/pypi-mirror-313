from mx_stream_core.data_sources.base import BaseDataSource
from pyspark.sql import Row, SparkSession


class MocEventDataSource(BaseDataSource):
    def __init__(self, spark: SparkSession, data, schema=None) -> None:
        self.data = data
        self.spark = spark
        self.schema = schema
        self.df = spark.createDataFrame(data, schema=schema)
        super().__init__()

    def foreach(self, func, processing_time=None):
        rows = []
        for item in self.data:
            rows.append(Row(**item))
        df = self.spark.createDataFrame(rows, schema=self.schema)
        func(df)

    def awaitTermination(self):
        pass
