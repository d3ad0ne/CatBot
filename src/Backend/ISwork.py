from minio import Minio
from random import randint
from datetime import timedelta
from src.Backend import DBwork
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
    objects = client.list_objects(config.bucket_name, prefix=currentDay+'/')
    return sum(1 for _ in objects)

def getObjectExtension(client, currentDay, fileNumber):
    objects = client.list_objects(config.bucket_name, prefix=currentDay+'/')
    for counter, obj in enumerate(objects, start=1):
        if counter == fileNumber:
            return obj.object_name.split('.')[-1]

def getImageName(currentDay, client):
    maxFiles = getNumberofObjects(client, currentDay)
    fileNumber = randint(1, maxFiles)
    fileExtension = '.' + getObjectExtension(client, currentDay, fileNumber)
    desiredFile = currentDay + '/' + str(fileNumber) + fileExtension
    return desiredFile

def getDownloadURL(currentDay):
    client = _setClient()
    object_name = getImageName(currentDay, client)
    url = client.presigned_get_object(
    config.bucket_name,
    object_name,
    expires=timedelta(days=1))
    return url

def downloadForAll(currentDay):
    cur, conn = DBwork.set_connection()
    max_id = DBwork.get_last_id(cur)
    for id in range(1, max_id + 1):
        chat_id = DBwork.get_chat_id(id, cur)
        image_URL = getDownloadURL(currentDay)
    DBwork.close_connection(conn, cur)

