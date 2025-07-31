from decouple import config


IS_address = config('IS_ADDRESS')
acc_key = config('ACC_KEY')
sec_key = config('SEC_KEY')
db_name = config('DB_NAME')
postgres_user = config('POSTGRES_USER')
postgres_password = config('POSTGRES_PASSWORD')
host_name = config('HOST_NAME')
port = config('PORT')
bucket_name = config('BUCKET_NAME')


TG_TOKEN = config('TG_TOKEN')
# ADMINS = [int(admin_id) for admin_id in config('ADMINS').split(',')]