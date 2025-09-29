from decouple import config

TG_token = config('TG_TOKEN')

IS_address = config('IS_ADDRESS')
acc_key = config('MINIO_ACCESS_KEY')
sec_key = config('MINIO_SECRET_KEY')
root_user = config('MINIO_ROOT_USER')
bucket_name = config('BUCKET_NAME')

db_name = config('DB_NAME')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')
host_name = config('POSTGRES_HOST_NAME')
port = config('POSTGRES_PORT')

logging_level = config('LOGGING_LEVEL')
