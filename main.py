from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from db_config.config import setting
from db_config.database import engine
from hash_model.models import Base
from routers import users, login, product, celery
from fastapi.middleware.cors import CORSMiddleware
from routers.celery import create_celery
from task import divide, image_upload

Base.metadata.create_all(bind=engine)

app = FastAPI(title=setting.TITLE,
              description=setting.DESCRIPTION,
              version=setting.VERSION,
              contact={
                  "name": setting.NAME,
                  "email": setting.EMAIL
              },
              openapi_tags=setting.TAGS,
              docs_url="/dipu")

app.celery_app = create_celery()
origins = ["http://localhost:3000", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post('/')
def home(image: UploadFile = File(default=None)):
    image_upload.delay(image)
    return {'status': "Success", "message": "Page Refresh"}

# @app.post('/')
# def home():
#     divide.delay(20, 100)
#     return {'status': "Success", "message": "Page Refresh"}

app.include_router(login.router) 
app.include_router(users.router)
app.include_router(product.router)
