import os
from mx_stream_core.config.s3 import s3_enable, s3_bucket, s3_folder, s3_dims_folder

delta_folder = os.getenv('DELTA_FOLDER', ".delta")
default_delta_path = f'{s3_bucket}/{s3_folder}/{delta_folder}' if s3_enable else '/tmp/.delta'
delta_path = os.getenv('DELTA_PATH', default_delta_path)

default_dims_delta_path = f'{s3_bucket}/{s3_dims_folder}' if s3_enable else '/tmp/dims/.delta'
dims_delta_path = os.getenv('DIMS_DELTA_PATH', default_dims_delta_path)

def get_dims_dsrc_delta_path(table_name=None) -> str:
    return f'{s3_dims_folder}/{table_name}'
