from minio import Minio
from random import randint
import dbwork

def _setClient():
    minio_client = Minio(
        "localhost:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
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
    counter = 1
    user = dbwork.get_user(counter)
    while(user != 'Error'):
        downloadImage(currentDay, user)
        counter += 1
        user = dbwork.get_user(counter)

Day = 'Tuesday'
downloadForAll(Day)