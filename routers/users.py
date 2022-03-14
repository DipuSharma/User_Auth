import re
from time import time
from unicodedata import name
from fastapi import APIRouter, Body, Depends, Query, Response, HTTPException, status, Request
from sqlalchemy import true
from schemas import UserCreate
from hash import Hash
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.encoders import jsonable_encoder
from database import get_db
from models import User
import os
from config import setting
from jose import jwt
from starlette.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")


conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL,
    MAIL_PASSWORD=PASS,
    MAIL_FROM=EMAIL,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

router = APIRouter()


@router.post('/registration', tags=["User"])
async def registration(user: UserCreate = Body(default=None), db: Session = Depends(get_db)):
    data = db.query(User).filter(User.email == user.email).first()
    if user.password == user.confirm_password:
        user = User(name=user.name, email=user.email, password=Hash.get_hash_pass(user.password))
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, user.email):
            return {"status":"failed","message": "Invalid Email ID Please Enter Valid Email"}
        if not data:
            if user:
                data = {"sub": user.email, "expiry":time() + 600 }
                jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
                # response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
                # print("Set Cookie")
                template = f"""
                    <!Doctype html>
                    <html>
                        <head>
                            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                            <style>

                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="row">
                                    <div class="col-md-3"></div>
                                    <div class="col-md-6">
                                        <h2>Account Verification</h2>
                                        <br>
                                        <p>Thanks for Choosing Myapp, please click on the given below Button </p>
                                        <a style="margin-top:1rem; padding:1rem; border-radius:0.5rem; font-size:1rem;
                                        text-decoration:none;
                                        background: red" href="http://localhost:3000/verification?token={jwt_token}">
                                        Verify Your Mail
                                        </a>
                                        <p>Please kidly ignore this email if you did not register for My app and nothing will happened.
                                        Thanks</p>
                                    </div>
                                    <div class="col-md-3"></div>
                                </div>
                            </div>
                        </body>
                    </html>
                    """
                message = MessageSchema(
                    subject="MyApp Account Verification Email",
                    recipients=[user.email],  # List of Recipients
                    body=template,
                    subtype="html"
                )
                fm = FastMail(conf)
                db.add(user)
                db.commit()
                db.refresh(user)
                await fm.send_message(message)
                return {"message": "Please Verify your Gmail, verification link send on your email account", "data": jwt_token}
            elif data.email == user.email:
                raise HTTPException(
                    status_code=status.HTTP_226_IM_USED,
                    detail="Email Already Exits Please do Registration to another Email"
                )
        else:
            return {"status":"failed","message":"Email Already Exists Please try to another email id"}
    else:
        return {"status": "failed", "message":"Password and Confirm Password Doesn't Match!!!!"}


@router.put("/verifytoken", tags=["User"])
async def email_verification(token: str = Query(default=None), db: Session = Depends(get_db)):
    if token:
        verified = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            email: str = verified.get("sub")
            existing_data = db.query(User).filter(User.email == email)
            if not existing_data.first():
                return {"message":"Email Verification Unsuccessfull...."}
            existing_data.update({"is_active": True})
            db.commit()
            return {"message": "Email Verification Successfully"}
        else:
            return {"status":"failed", "message":"token expires please re-registration"}
    else:
        return {"status":"failed", "message":"Token Not Found"}

