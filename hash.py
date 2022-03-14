from fastapi import HTTPException, status, Response
from passlib.context import CryptContext
from config import setting
from models import User
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def get_hash_pass(plain_password):
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)

