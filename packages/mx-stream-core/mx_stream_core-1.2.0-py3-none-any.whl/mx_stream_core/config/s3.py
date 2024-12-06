import os

s3_access_key = os.getenv('S3_ACCESS_KEY', 'minio')
s3_secret_key = os.getenv('S3_SECRET_KEY', 'minio123')
s3_endpoint = os.getenv('S3_ENDPOINT', 'http://localhost:9000')
s3_bucket = os.getenv('S3_BUCKET', 'cdp')
s3_enable = os.getenv('S3_ENABLE', 'true')
s3_folder = os.getenv('S3_FOLDER', 'data')
s3_dims_folder = os.getenv('S3_DIMS_PATH', f'{s3_bucket}/dims/.delta')
