from celery import shared_task
from time import sleep
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import UploadFile, File
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")


conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL,
    MAIL_PASSWORD=PASS,
    MAIL_FROM=EMAIL,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


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
    return c

@shared_task
def image_upload(x):
    try:
        dir_path = os.getcwd()+"/static/images/"
        if dir_path is None:
            os.mkdir("static/images")
        else:
            file_name = os.getcwd()+"/static/images/"+x.filename.replace(" ", "-")
            with open(file_name,'wb+') as f:
                f.write(x.file.read())
                f.close()
            file = jsonable_encoder({"imagePath":file_name})
            return {"filename": file_name}
    except Exception as e: 
        return None