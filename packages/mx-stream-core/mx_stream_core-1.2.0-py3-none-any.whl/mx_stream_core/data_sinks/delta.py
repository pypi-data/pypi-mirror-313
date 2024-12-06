from delta import DeltaTable
from mx_stream_core.infrastructure.spark import spark
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, last

from .base import BaseDataSink


class DeltaDataSink(BaseDataSink):
    def __init__(self, delta_location: str, schema=None) -> None:
        self.delta_location = delta_location
        self.schema = schema

    def put(self, df: DataFrame) -> None:
        df.write.format('delta').option('mergeStream', "true").mode('append').save(self.delta_location)

    def get_schema(self):
        return self.schema

    def upsert(self, new_df: DataFrame, sets=None, condition="current.id = new.id") -> None:
        schema = self.schema if self.schema else new_df.schema

        try:
            delta_table = DeltaTable.forPath(spark, self.delta_location)
        except:
            spark.createDataFrame([], schema).write.format('delta').mode('overwrite').save(self.delta_location)
            delta_table = DeltaTable.forPath(spark, self.delta_location)

        all_columns = new_df.columns
        all_columns.remove('id')
        agg_exprs = [last(col).alias(col) for col in all_columns]
        new_df = new_df.groupBy("id").agg(*agg_exprs)

        for field in schema.fields:
            if field.name not in new_df.columns:
                new_df = new_df.withColumn(field.name, lit(None).cast(field.dataType))

        delta_table.alias("current") \
            .merge(
            source=new_df.alias("new"),
            condition=condition) \
            .whenMatchedUpdate(set=sets) \
            .whenNotMatchedInsertAll() \
            .execute()

        # Ensure the data is written before proceeding (blocking action)
        spark.read.format("delta").load(self.delta_location).count()
