from minio import Minio
from random import randint
import DBwork
import config

def _setClient():
    minio_client = Minio(
        config.IS_address,
        access_key = config.acc_key,
        secret_key = config.sec_key,
        secure = False
    )
    return minio_client

def getImageName(currentDay):
    maxFiles = 2
    fileNumber = randint(1, maxFiles)
    desiredFile = currentDay + '/' + str(fileNumber) + '.jpeg'
    return desiredFile

def downloadImage(currentDay, username):
    bucket_name = "cat-images"
    client = _setClient()
    client.fget_object(bucket_name, getImageName(currentDay), username + '.jpeg')

def downloadForAll(currentDay):
    cur, conn = DBwork.set_connection()
    counter = 1
    user = DBwork.get_user(counter, cur)
    while(user != 'Error'):
        downloadImage(currentDay, user)
        counter += 1
        user = DBwork.get_user(counter, cur)
    DBwork.close_connection(conn, cur)

