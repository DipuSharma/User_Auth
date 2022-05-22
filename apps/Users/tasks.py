import os
from time import sleep
import asyncio
from celery import shared_task
from fastapi.encoders import jsonable_encoder
from celery.utils.log import get_task_logger
from tqdm import tqdm, trange

from apps.product.product import BASE_DIR

logger = get_task_logger(__name__)

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def operation(x, y, o):
    sleep(2)
    if o == "add":
        c = x + y
    if o == "sub":
        c = x - y
    if o == "multi":
        c = x * y
    if o == "devide":
        c = x / y
    logger.info('Adds {0} + {1}'.format(x, y))
    return c

@shared_task
def any_file_upload(files):
    File_DIR = './static/files/'
    if not os.path.exists(File_DIR):
        os.makedirs(File_DIR)
    file_name = File_DIR + files.filename
    print("Hello Dipu")
    with open(file_name,'wb+') as f:
        f.write(files.file.read())
        f.close()
    return True

@shared_task
def image_upload(files):
    File_DIR = './static/images/'
    if not os.path.exists(File_DIR):
        os.makedirs(File_DIR)
    file_name = File_DIR + files.filename
    print("Hello Dipu")
    with open(file_name,'wb+') as f:
        f.write(files.file.read())
        f.close()
    return True