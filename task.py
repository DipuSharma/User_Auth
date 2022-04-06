from sre_constants import SUCCESS
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


# @shared_task(serializer='json')
# async def send_mail_task():
#     message = MessageSchema(
#         subject="MyApp Account Verification Email",
#         recipients=["sdipu231@gmail.com"],  # List of Recipients
#         body="Hello Dipu Your welcome",
#     )
#     fm = FastMail(conf)
#     fm.send_message(message)
#     return None

@shared_task
def divide(x, y):
    sleep(5)
    return x + y

@shared_task
def image_upload(x):
    try:
        os.mkdir("static/images")
    except Exception as e: 
        file_name = os.getcwd()+"/static/images/"+x.filename.replace(" ", "-")
        with open(file_name,'wb+') as f:
            f.write(x.file.read())
            f.close()
        file = jsonable_encoder({"imagePath":file_name})
        # new_image = await add_image(file)
        return {"filename": file_name}  