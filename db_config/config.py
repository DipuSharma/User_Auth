import pathlib
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")
ALGO = os.getenv("ALGO")


class Settings:
    TITLE = "My App"
    VERSION = "0.0.0.1"
    DESCRIPTION = """
        This is my application created in Fastapi
        It has only one route "index"
        """
    NAME = "Dipu Kumar Sharma"
    EMAIL = EMAIL
    PASS = PASS
    TAGS = [
        {"name": "Auth", "description": "This is Authentication Routes"},
        {"name": "User", "description": "This is user routes"},
        {"name": "Product", "description": "This is Product routes"},
        {"name": "Default", "description": "This is Default routes"},
        {"name": "Cart", "description": "This is Cart routes"},
        {"name": "Shop", "description": "This is Shopkeeper Routes"},
        {"name": "Home", "description": "This is Home Routes"}
    ]
    SECRET_KEY = "Sv/w?/T@^CN8RR$O8^I7Tss6'j76it"
    ALGORITHM = ALGO
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    accept_content = ['pickle','application/json']
    task_serializer = 'pickle'
    result_serializer = 'pickle'

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
    DATABASE_CONNECT_DICT: dict = {}

    broker_url: str = os.environ.get("broker_urls", "redis://127.0.0.1:6379/0")
    result_backend: str = os.environ.get("result_backend", "redis://127.0.0.1:6379/0")


setting = Settings()
