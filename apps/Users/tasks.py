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
    sleep(.1)
    if o == "add":
        c = x + y
    if o == "sub":
        c = x - y
    if o == "multi":
        c = x * y
    if o == "devide":
        c = x / y
    # for i in tqdm(range(0, 100)):pass
    return c

@shared_task
def file_upload(x):
    return "Done"

def any_file_upload(file, file_size):
    File_DIR = './static/files/'
    if not os.path.exists(File_DIR):
        os.makedirs(File_DIR)
    file_name = File_DIR + file.filename
    in_mb = file_size / 1024
    with open(file_name,'wb+') as f:
        f.write(file.file.read())
        f.close()
    for i in tqdm(range(0, int(in_mb))):
        sleep(.01)
    file_upload.delay(in_mb)

@shared_task
def image_upload(files):
    File_DIR = './static/profile_image/'
    if not os.path.exists(File_DIR):
        os.makedirs(File_DIR)
    file_name = File_DIR + files.filename
    with open(file_name,'wb+') as f:
        f.write(files.file.read())
        f.close()
    print(len(files.file.read()))
    return True