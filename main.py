from fastapi import FastAPI
from db_config.config import setting
from db_config.database import engine
from models import Base
from routers import users, login, product
from fastapi.middleware.cors import CORSMiddleware

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

origins = ["http://localhost:3000", "http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.post('/')
async def home():
    return {'status': "Success", "message": "Page Refresh"}

app.include_router(login.router)
app.include_router(users.router)
app.include_router(product.router)
