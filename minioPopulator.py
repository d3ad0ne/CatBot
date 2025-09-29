import glob
import os

from minio import Minio
from minio.error import S3Error


def upload_image(bucket_name, object_name, file_path):
    try:
        if file_path.split('.')[-1] == 'jpeg':
            client.fput_object(bucket_name, object_name, file_path, 'image/jpeg')
            print(f'image {object_name} with local path \'{file_path}\' was successfully uploaded')
        elif file_path.split('.')[-1] == 'jpg':
            client.fput_object(bucket_name, object_name, file_path, 'image/jpg')
            print(f'image {object_name} with local path \'{file_path}\' was successfully uploaded')
        elif file_path.split('.')[-1] == 'png':
            client.fput_object(bucket_name, object_name, file_path, 'image/png')
            print(f'image {object_name} with local path \'{file_path}\' was successfully uploaded')
        elif file_path.split('.')[-1] == 'pjpeg':
            client.fput_object(bucket_name, object_name, file_path, 'image/pjpeg')
            print(f'image {object_name} with local path \'{file_path}\' was successfully uploaded')

    except S3Error as e:
        print(f'Error during MinIO operation: {e}')


# Main

print('Please enter your MinIO instance cloud address:')
IS_address = input()
print('Please enter MinIO access key:')
access_key = input()
print('Please enter MinIO secret key:')
secret_key = input()
print('Please enter bucket name:')
bucket = input()


client = Minio(
    IS_address,
    access_key=access_key,
    secret_key=secret_key,
    secure=False
)

is_found = client.bucket_exists(bucket)
if not is_found:
    client.make_bucket(bucket)
    print(f"Bucket '{bucket}' does not exist. A new bucket with that name have been created.")
else:
    print(f"Bucket '{bucket}' exists. Proceeding...")

script_path = os.path.abspath(__file__).replace('\\', '/')
for i in range(len(script_path) - 1, 0, -1):
    if script_path[i] == '/':
        script_path = script_path[:i + 1]
        break
paths = glob.glob(script_path + '*')
inter_paths, shortened_paths = [], []

for i in range(len(paths)):
    paths[i] = os.path.abspath(paths[i]).replace('\\', '/')

for index, path in enumerate(paths, 0):
    for j in range(len(path) - 1, 0, -1):
        if path[j] == '/':
            inter_paths.append(paths[index][j:])

for path in inter_paths:
    if path.count('/') == 1 and (path[-3:] == 'jpg' or path[-3:] == 'png' or path[-4:] == 'jpeg' or path[-5:] == 'pjpeg'):
        shortened_paths.append(path)

c = 0
for i in range(len(paths)):
    i -= c
    if not('.jpg' in paths[i] or '.jpeg' in paths[i] or '.pjpeg' in paths[i] or '.png' in paths[i]):
        del paths[i]
        c += 1
    if len(paths) < i:
        break

starting_weekday = 0
prev_obj_len = -1
for n in range(1, 8):
    objects = client.list_objects(bucket, prefix=str(n) + '/')
    obj_len = sum(1 for _ in objects)
    if n == 1:
        if obj_len < sum(1 for _ in client.list_objects(bucket, prefix='7/')):
            starting_weekday = n - 1
    elif prev_obj_len > obj_len:
        starting_weekday = n - 1
        break
    prev_obj_len = obj_len

for i in range(0, len(shortened_paths)):
    weekday = (i + starting_weekday) % 7 + 1
    upload_image(bucket, str(weekday) + shortened_paths[i], paths[i])
