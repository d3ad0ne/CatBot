from minio import Minio
from random import randint
from datetime import timedelta
from src import config


def _setClient():
    minio_client = Minio(
        config.IS_address,
        access_key = config.acc_key,
        secret_key = config.sec_key,
        secure = False
    )
    return minio_client


def getNumberofObjects(client, currentDay):
    objects = client.list_objects(config.bucket_name, prefix=str(currentDay) + '/')
    return sum(1 for _ in objects)


def getObjectExtension(client, currentDay, fileNumber):
    objects = client.list_objects(config.bucket_name, prefix=str(currentDay) + '/')
    counter = 0
    object_extension = None
    for obj in objects:
        counter += 1
        if counter == fileNumber:
            object_extension = obj.object_name.split('.')[-1]
    return object_extension


def getImageName(currentDay, client):
    maxFiles = getNumberofObjects(client, currentDay)
    fileNumber = randint(1, maxFiles)
    fileExtension = '.' + getObjectExtension(client, currentDay, fileNumber)
    desiredFile = str(currentDay) + '/' + str(fileNumber) + fileExtension
    return desiredFile


def getDownloadURL(currentDay):
    client = _setClient()
    object_name = getImageName(currentDay, client)
    url = client.presigned_get_object(
    config.bucket_name,
    object_name,
    expires=timedelta(days=1)
    )
    return url
