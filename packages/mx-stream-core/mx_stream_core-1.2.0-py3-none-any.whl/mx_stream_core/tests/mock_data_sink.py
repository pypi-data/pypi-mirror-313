from pyspark.sql import DataFrame
from mx_stream_core.data_sinks.base import BaseDataSink
from pyspark.sql.functions import col


class MockDataSink(BaseDataSink):
    def __init__(self, spark=None, schema=None, current_data_source=None) -> None:
        if current_data_source is None:
            current_data_source = []
        self.schema = schema
        self.df: DataFrame = None
        if schema is not None and spark is not None:
            self.df = spark.createDataFrame(current_data_source, schema=schema)

        super().__init__()

    def put(self, df: DataFrame) -> None:
        if self.schema is None and self.df is None:
            self.df = df
        else:
            self.df = self.df.union(df)

    def show(self):
        if self.df:
            self.df.show()

    def upsert(self, new_df: DataFrame, sets=None, condition="current.id = new.id") -> DataFrame:
        combined_product_items_df = new_df.select(
            *[col(col_name).alias(col_name) for col_name in new_df.columns],
        ).alias('new')
        current_column = self.df.columns
        current_column.remove('id')
        merged_df = self.df.alias('current').join(
            combined_product_items_df,
            self.df['id'] == combined_product_items_df['id'],
            'outer'
        ).selectExpr(
            'COALESCE(current.id, new.id) as id',
            *[f"COALESCE(new.{col_name}, current.{col_name}) as {col_name}" for col_name in current_column]
        )
        self.df = merged_df
        return self.df

    def get(self) -> DataFrame:
        return self.df
