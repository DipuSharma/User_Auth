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
        {"name": "User", "description": "This is user routes"},
        {"name": "Product", "description": "This is Product routes"},
        {"name": "Default", "description": "This is Default routes"}
    ]
    SECRET_KEY = "Sv/w?/T@^CN8RR$O8^I7Tss6'j76it"
    ALGORITHM = ALGO


setting = Settings()
