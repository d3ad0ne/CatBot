from minio import Minio
from random import randint
import DBwork
from src import config


def _setClient():
    minio_client = Minio(
        config.IS_address,
        access_key = config.acc_key,
        secret_key = config.sec_key,
        secure = False
    )
    return minio_client

def getNumberofObjects(client, currentDay, bucket_name):
    objects = client.list_objects(bucket_name, prefix=currentDay+'/')
    return sum(1 for _ in objects)

def getImageName(currentDay, client):
    maxFiles = getNumberofObjects(client, currentDay, config.bucket_name)
    fileNumber = randint(1, maxFiles)
    desiredFile = currentDay + '/' + str(fileNumber) + '.jpeg'
    return desiredFile

def downloadImage(currentDay, username):
    client = _setClient()
    client.fget_object(config.bucket_name, getImageName(currentDay, client), username + '.jpeg')

def downloadForAll(currentDay):
    cur, conn = DBwork.set_connection()
    max_id = DBwork.get_last_id(cur)
    for id in range(1, max_id + 1):
        user = DBwork.get_user(id, cur)
        downloadImage(currentDay, user)
    DBwork.close_connection(conn, cur)

