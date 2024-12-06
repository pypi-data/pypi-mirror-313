import os
from pyspark.sql import SparkSession

from mx_stream_core.config.app import app_name
from mx_stream_core.config.s3 import s3_access_key, s3_secret_key, s3_endpoint, s3_enable, s3_bucket, s3_folder
from mx_stream_core.config.spark import master_url, spark_memory_usage, spark_memory_overhead

spark_builder = SparkSession.builder.appName(app_name).master(master_url) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

if s3_enable == 'true':
    spark_builder.config("spark.hadoop.fs.s3a.access.key", s3_access_key) \
        .config("spark.hadoop.fs.s3a.secret.key", s3_secret_key) \
        .config("spark.hadoop.fs.s3a.endpoint", s3_endpoint) \
        .config("spark.hadoop.fs.s3a.fast.upload", "true") 

if spark_memory_usage:
    spark_builder.config("spark.executor.memory", spark_memory_usage) \
        .config("spark.driver.memory", spark_memory_usage) \
        .config("spark.executor.extraJavaOptions", os.getenv('SPARK_EXTRA_JAVA', "-XX:+UseG1GC")) \
        .config("spark.driver.extraJavaOptions", os.getenv('SPARK_EXTRA_JAVA', "-XX:+UseG1GC"))

if spark_memory_overhead:
    spark_builder.config("spark.executor.memoryOverhead", spark_memory_overhead) \
        .config("spark.driver.memoryOverhead", spark_memory_overhead)

spark = spark_builder.getOrCreate()
spark.sparkContext.setLogLevel(os.getenv('LOG_LEVEL', 'WARN'))

checkpoint_folder = os.getenv('CHECKPOINT_FOLDER', ".checkpoints")
default_root_checkpoint_path = f'{s3_bucket}/{s3_folder}/{checkpoint_folder}' if s3_enable else '/tmp/.checkpoints'
root_check_point_path = os.getenv(
    'CHECKPOINT_PATH', default_root_checkpoint_path)


def get_checkpoint_path(table_name=None) -> str:
    if table_name is not None:
        return f"{root_check_point_path}/{table_name}_checkpoint"
    return f"{root_check_point_path}/checkpoint"
