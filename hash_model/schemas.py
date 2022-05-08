import email
from lib2to3.pgen2.token import OP
from unicodedata import category, name
from xmlrpc.client import Boolean, boolean
from fastapi import File, Form, UploadFile
from pydantic import EmailStr, BaseModel, HttpUrl
from typing import List, Optional

# User Schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    class Config:
        orm_mode: True

class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode: True

class EmailSchema(BaseModel):
    email: List[EmailStr]

class ForgatPassword(BaseModel):
    email:str

class VerifyOTP(BaseModel):
    otp:str

class ResetPassword(BaseModel):
    token: str
    password: str
    confirm_password: str

#  Product Schema

class ProductImage(BaseModel):
    product_name: str
    url = HttpUrl
    
    class Config:
        orm_mode:True

class CreateProduct(BaseModel):
    product_name : str
    description: Optional[str]
    price: Optional[float]
    d_price: Optional[float]
    size: Optional[str]

    class Config:
        orm_mode: True

class SearchProduct(BaseModel):
    product_name: Optional[str] = None
    size: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    class Config:
        orm_mode: True
    

class ShowProduct(BaseModel):
    id: int
    owner_id: int

    class Config:
        orm_mode: True