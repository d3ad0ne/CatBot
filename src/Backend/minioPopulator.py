from minio import Minio
from minio.error import S3Error
from src import config
import glob
import os


access_key = config.acc_key
secret_key = config.sec_key
bucket = config.bucket_name


def upload_file(access_key, secret_key, bucket_name, object_name, file_path):
    try:
        client = Minio(
            config.IS_address,
            access_key = access_key,
            secret_key = secret_key,
            secure = False
        )
        if file_path.split('.')[-1] == 'jpeg':
            client.fput_object(bucket_name, object_name, file_path, 'image/jpeg')
        if file_path.split('.')[-1] == 'jpg':
            client.fput_object(bucket_name, object_name, file_path, 'image/jpg')
        elif file_path.split('.')[-1] == 'png':
            client.fput_object(bucket_name, object_name, file_path, 'image/png')
        elif file_path.split('.')[-1] == 'pjpeg':
            client.fput_object(bucket_name, object_name, file_path, 'image/pjpeg')
        print(f'image {object_name} with local path \'{file_path}\' was successfully uploaded')

    except S3Error:
        print(f'Error during MinIO operation: {S3Error}')


paths = glob.glob('../../files/*/*')
shortened_paths = []

for i in range(len(paths)):
    paths[i] = os.path.abspath(paths[i]).replace('\\', '/')

for i in range(len(paths)):
    shortened_paths.append(paths[i][paths[i].find('files/') + 6:])

# for i in range(0, len(paths)):
#     upload_file(access_key, secret_key, bucket, f'{shortened_paths[i]}', f'{paths[i]}')
#     print(paths[i])



client = Minio(
        config.IS_address,
        access_key = access_key,
        secret_key = secret_key,
        secure = False
    )
objects = client.list_objects(config.bucket_name, prefix='1' + '/')
for obj in objects:
    print(obj.object_name)
