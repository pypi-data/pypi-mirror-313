from pyspark.sql import DataFrame


class BaseDataSink:
    def put(self, df: DataFrame) -> None:
        raise NotImplementedError('Not implemented')

    def upsert(self, new_df: DataFrame, sets=None, condition="current.id = new.id") -> None:
        raise NotImplementedError('Not implemented')

    def get_spark(self):
        raise NotImplementedError('Not implemented')

    def get_schema(self):
        raise NotImplementedError('Not implemented')
