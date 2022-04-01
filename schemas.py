import email
from lib2to3.pgen2.token import OP
from unicodedata import name
from xmlrpc.client import Boolean, boolean
from fastapi import File, UploadFile
from pydantic import EmailStr, BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode: True


class EmailSchema(BaseModel):
    email: List[EmailStr]

class CreateProduct(BaseModel):
    name : str
    description: Optional[str]
    price: float
    d_price: float

class ForgatPassword(BaseModel):
    email:str

class VerifyOTP(BaseModel):
    otp:str

class ResetPassword(BaseModel):
    token: str
    password: str
    confirm_password: str

class ShowProduct(BaseModel):
    id: int
    owner_id: int

    class Config:
        orm_mode: True