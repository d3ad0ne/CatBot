from decouple import config


IS_address = config('IS_ADDRESS')
acc_key = config('MINIO_ACCESS_KEY')
sec_key = config('MINIO_SECRET_KEY')
root_user = config('MINIO_ROOT_USER')
db_name = config('DB_NAME')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')
host_name = config('HOST_NAME')
port = config('PORT')
bucket_name = config('BUCKET_NAME')

TG_token = config('TG_TOKEN')
# ADMINS = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging_level = config('LOGGING_LEVEL')