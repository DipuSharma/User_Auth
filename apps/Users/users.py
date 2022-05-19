import re
import os
import random
from urllib import response
import pdfkit
from time import time
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import APIRouter, Body, Depends, Query, File, HTTPException, Response, status, UploadFile
from sqlalchemy import true
from hash_model.schemas import UserCreate, ForgatPassword, ResetPassword,VerifyOTP
from hash_model.hash import Hash
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi.encoders import jsonable_encoder
from db_config.database import get_db
from hash_model.models import User, OTP
from db_config.config import setting
from jose import jwt
from dotenv import load_dotenv
from apps.auth.login import oauth2_scheme


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
        user = User(name=user.name, email=user.email, type=user.user_type,password=Hash.get_hash_pass(user.password))
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, user.email):
            return {"status":"failed","message": "Invalid Email ID Please Enter Valid Email"}
        if not data:
            if user:
                data = {"sub": user.email, "expiry":time() + 600 }
                jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
                # response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
                # print("Set Cookie")
                # template = f"""
                #     <!Doctype html>
                #     <html>
                #         <head>
                #             <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                #             <style>

                #             </style>
                #         </head>
                #         <body>
                #             <div class="container">
                #                 <div class="row">
                #                     <div class="col-md-3"></div>
                #                     <div class="col-md-6">
                #                         <h2>Account Verification</h2>
                #                         <br>
                #                         <p>Thanks for Choosing Myapp, please click on the given below Button </p>
                #                         <a style="margin-top:1rem; padding:1rem; border-radius:0.5rem; font-size:1rem;
                #                         text-decoration:none;
                #                         background: red" href="http://localhost:3000/verification?token={jwt_token}">
                #                         Verify Your Mail
                #                         </a>
                #                         <p>Please kidly ignore this email if you did not register for My app and nothing will happened.
                #                         Thanks</p>
                #                     </div>
                #                     <div class="col-md-3"></div>
                #                 </div>
                #             </div>
                #         </body>
                #     </html>
                #     """
                # message = MessageSchema(
                #     subject="MyApp Account Verification Email",
                #     recipients=[user.email],  # List of Recipients
                #     body=template,
                #     subtype="html"
                # )
                # fm = FastMail(conf)
                db.add(user)
                db.commit()
                db.refresh(user)
                # await fm.send_message(message)
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

@router.post("/profile/", tags=["User"])
async def image_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        os.mkdir("static/images")
    except Exception as e: 
        file_name = os.getcwd()+"/static/images/"+file.filename.replace(" ", "-")
        with open(file_name,'wb+') as f:
            f.write(file.file.read())
            f.close()
        return {"filename": file_name}       

@router.put("/verify-email", tags=["User"])
async def email_verification(token: str = Query(default=None), db: Session = Depends(get_db)):
    if token:
        verified = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            email: str = verified.get("sub")
            existing_data = db.query(User).filter(User.email == email)
            if not existing_data.first():
                return {"status":"failed","message":"Email Verification Unsuccessfull...."}
            else:
                existing_data.update({"is_active": True})
                db.commit()
                return {"message": "Email Verification Successfully"}
        else:
            return {"status":"failed", "message":"token expires please re-registration"}
    else:
        return {"status":"failed", "message":"Token Not Found"}

@router.post("/forgat-password", tags=["User"])
async def forgat_pass(user:ForgatPassword = Body(default=None), db: Session = Depends(get_db)):
    data =  db.query(User).filter(User.email == user.email and User.is_active == True).first()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not data:
        return {"status": "failed", "message":"Details Not Found"}
    if not re.fullmatch(regex, user.email):
            return {"status":"failed","message": "Invalid Email ID Please Enter Valid Email"}  
    if user.email == data.email:
        otp = ''.join([str(random.randint(0, 9)) for i in range(6)])
        user_entry = OTP(email=user.email, otp=otp, exp_time=time() + 60, count_otp= 1)
        otp_email =  db.query(OTP).filter(OTP.email == user.email).first()
        if not otp_email:
            db.add(user_entry)
            db.commit()
            db.refresh(user_entry)
            message = MessageSchema(
                subject="MyApp Account Verification Email",
                recipients=[user.email],  # List of Recipients
                body=f"your otp is {otp}"
            )
            fm = FastMail(conf)
            await fm.send_message(message)
            return {"status": "Ok", "message":"Otp send on your mail id"}
        existing_data = db.query(OTP).filter(OTP.email == user.email)
        if user.email == otp_email.email:
            num = int(otp_email.count_otp)
            if num < 3:
                num = num + 1
                existing_data.update({"otp": otp, "status":False, "exp_time":time() + 60, "count_otp": num})
                db.commit()
                message = MessageSchema(
                    subject="MyApp Account Verification Email",
                    recipients=[user.email],  # List of Recipients
                    body=f"your otp is {otp}",
                )
                fm = FastMail(conf)
                await fm.send_message(message)
                return {"status":"failed", "message":"Otp send on your mail id please verified"}
            else:
                return {"status":"failed", "message":"your Ip is blocked"}
        else:
            return {"status":"failed", "message":"Please Generate Otp again"}
    else:
        return {"status":"failed", "message":"Details Not Found"}
   
@router.put("/reset-password", tags=["User"])
async def reset_pass(user: ResetPassword = Body(default=None), db: Session = Depends(get_db)):
    if user.token:
        verified = jwt.decode(user.token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        print(verified)
        if verified['expiry'] >= time():
            email: str = verified.get("sub")
            existing_data = db.query(User).filter(User.email == email and User.is_active == True)
            if not existing_data.first():
                return {"status":"failed","message":"Password Reset Failed"}
              
            if user.password != user.confirm_password:
                return {"status":"failed", "message":"Password and Confirm Password mismatch"}

            password=Hash.get_hash_pass(user.password)
            existing_data.update({"password": password})
            db.commit()
            return {"message": "Password Reset Successfully"}
        else:
            return {"status":"failed", "message":"please generate otp "}
    else:
        return {"status":"failed", "message":"Details Not Found"}

@router.post("/verify-otp", tags=["User"])
async def verify_otp(user:VerifyOTP = Body(default=None), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=404, detail="Otp not found")
    data = db.query(OTP).filter(OTP.otp == user.otp).first()
    existing_data = db.query(OTP).filter(OTP.otp == user.otp)
    if not data:
        return {"status":"failed", "message":"Invalid OTP please enter valid Otp"}
    otp_db_time = float(data.exp_time)
    num = 1
    if data.otp == user.otp and otp_db_time >= time():
        data = {"sub": data.email, "expiry":time() + 600}
        jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
        existing_data.update({"status": True, "count_otp": num })
        db.commit()
        return {"status":"success", "token": jwt_token}
    else:
        existing_data.update({"count_otp": num })
        db.commit()
        return {"status": "failed", "msg":"Otp Expired"}

@router.get("/me", tags=['User'])
async def curren_user(db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verified = jwt.decode(token, setting.SECRET_KEY,algorithms=setting.ALGORITHM)
    if verified['expiry'] >= time():
        user = db.query(User).filter(User.email == verified['sub'] and User.type == verified['type']).first()
        if not user:
            raise HTTPException(status_code=404, detail="Address not found of this user")
        print(user.address)
        return {"status":"success", "data":user}
    else:
        return {"status": "failed", "message": "You are not authorized"}


@router.get("/generate-pdf", tags=["User"])
async def generate_pdf(
    # db:Session = Depends(get_db), 
    # token: str = Depends(oauth2_scheme)
    ):
    # verified = jwt.decode(token, setting.SECRET_KEY,algorithms=setting.ALGORITHM)
    # if verified['expiry'] >= time():
    #     user = db.query(User).filter(User.email == verified['sub'] and User.type == verified['type']).first()
    #     if not user:
    #         raise HTTPException(status_code=404, detail="Address not found of this user")
        
    # else:
    #     return {"status": "failed", "message": "You are not authorized"}
    path_dir = os.getcwd()
    file_data = os.path.join(path_dir, "static/view/pdf.html")
    pdf = pdfkit.from_url(file_data, False)
    response = Response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers["Content-Disposition"] = f"attachment; filename=demonew.pdf"
    return response