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
        {"name": "Employee", "description": "This is employee routes"}
    ]
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASS = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "mydb")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    SECRET_KEY = "Sv/w?/T@^CN8RR$O8^I7Tss6'j76it"
    ALGORITHM = ALGO


setting = Settings()
