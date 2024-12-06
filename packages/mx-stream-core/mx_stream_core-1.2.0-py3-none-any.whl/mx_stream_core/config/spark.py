import os

from mx_stream_core.config.s3 import s3_enable, s3_bucket, s3_folder

master_url = os.getenv('MASTER_URL', "local[*]")

checkpoint_folder = os.getenv('CHECKPOINT_FOLDER', ".checkpoints")
default_root_checkpoint_path = f'{s3_bucket}/{s3_folder}/{checkpoint_folder}' if s3_enable else '/tmp/.checkpoints'
root_check_point_path = os.getenv('CHECKPOINT_PATH', default_root_checkpoint_path)

spark_memory_usage = os.getenv('SPARK_MEMORY_USAGE')
spark_memory_overhead = os.getenv('SPARK_MEMORY_OVERHEAD')

def get_checkpoint_path(table_name=None) -> str:
    if table_name is not None:
        return f"{root_check_point_path}/{table_name}_checkpoint"
    return f"{root_check_point_path}/checkpoint"
