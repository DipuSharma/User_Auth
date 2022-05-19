import email
from lib2to3.pgen2.token import OP
from unicodedata import category, name
from xmlrpc.client import Boolean, boolean
from fastapi import File, Form, UploadFile
from pydantic import EmailStr, BaseModel, HttpUrl
from typing import List, Optional

# User Schema
class UserCreate(BaseModel):
    user_type: Optional[str]
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    class Config:
        orm_mode: True

class LoginUser(BaseModel):
    user_type: str
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

#  Shopkeeper Schema
class AddressCreate(BaseModel):
    shop_name: Optional[str]
    register_number: Optional[str]
    gst_number: Optional[str]
    mobile_number: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    country_name: Optional[str]
    state: Optional[str]
    district: Optional[str]
    zipcode:Optional[str]

    class Config:
        orm_mode: True

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

class ShowShopSchema(BaseModel):
    shop_name: Optional[str]
    address:Optional[str]
    email: Optional[str]
    mobile_number:Optional[str]
    gst_number:Optional[str]

    class Config:
        orm_mode: True
    
class ShowProduct(BaseModel):
    id: int
    owner_id: int

    class Config:
        orm_mode: True