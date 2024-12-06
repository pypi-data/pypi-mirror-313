from mx_stream_core.data_sources.base import BaseDataSource
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession


class MockDataSource(BaseDataSource):
    def __init__(self, spark: SparkSession, data, schema) -> None:
        self.spark = spark
        self.data = data
        self.schema = schema
        self.df = spark.createDataFrame(data, schema=schema)
        super().__init__()

    def get(self) -> DataFrame:
        return self.df
