from datetime import timedelta
from random import randint

from loguru import logger
from minio import Minio, S3Error

from src import config

logging_level = config.logging_level
logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level=logging_level
)


def _setClient():
    try:
        minio_client = Minio(
            config.IS_address, # type: ignore
            access_key = config.acc_key, # type: ignore
            secret_key = config.sec_key, # type: ignore
            secure = False
        )
        logger.info('Successfully set connection to the MinIO bucket')
        return minio_client
    except S3Error as e:
        logger.error(f'S3 error during connection to bucket. Code: {e.code}, Message: {e.message}')


def getNumberofObjects(client, currentDay):
    objects = client.list_objects(config.bucket_name, prefix=str(currentDay) + '/')
    numberOfObjects = sum(1 for _ in objects)
    return numberOfObjects


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
    if maxFiles == 0:
        return None
    fileNumber = randint(1, maxFiles)
    shortExtension = getObjectExtension(client, currentDay, fileNumber)
    fileExtension = ''
    if shortExtension is not None:
        fileExtension = '.' + shortExtension
    desiredFile = str(currentDay) + '/' + str(fileNumber) + fileExtension
    return desiredFile


def getDownloadURL(currentDay):
    client = _setClient()
    if client is None:
        logger.error("Failed to set MinIO client")
        return None

    object_name = getImageName(currentDay, client)
    if object_name is None:
        logger.error(f"Can't generate a URL: no files in current MinIO directory({currentDay})")
        return None

    url = client.presigned_get_object(
        config.bucket_name, # type: ignore
        object_name,
        expires=timedelta(days=1)
    )
    return url
