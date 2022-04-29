from fastapi import APIRouter
from db_config.constant import PREFIXES_API
from routers.users import router as user_router
api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix=PREFIXES_API.USER,
    tags=['User']
)