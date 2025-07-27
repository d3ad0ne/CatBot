from decouple import config


IS_address = config('IS_address')
acc_key = config('acc_key')
sec_key = config('sec_key')
db_name = config('db_name')
postgres_user = config('postgres_user')
postgres_password = config('postgres_password')
host_name = config('host_name')
port = config('port')
bucket_name = 'cat-images'


TG_TOKEN = config('TG_TOKEN')
# ADMINS = [int(admin_id) for admin_id in config('ADMINS').split(',')]