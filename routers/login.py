from time import time
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from db_config.database import get_db
from hash_model.models import User
from hash_model.hash import Hash
from jose import jwt
from db_config.config import setting
from hash_model.schemas import LoginUser
import re

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

router = APIRouter()


@router.post('/login', tags=['User'])
def login(response: Response, form: LoginUser = Body(default=None), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.email).first()
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username please enter valid username"
        )
    if not Hash.verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password please enter valid password"
        )
    if user.is_active == False:
        existing_item = db.query(User).filter(User.email == user.email)
        existing_item.delete()
        db.commit()
        return {"status":"failed", "message":"You are not verified user please do re-registration"}
    if len(form.password) < 6:
        return {"error": "Password is less than 6 Character, Please enter Password more thane 5 Character"}
    if not re.fullmatch(regex, form.email):
        return {"error": "Invalid Email ID Please Enter Valid Email"}
        
    if Hash.verify_password(form.password, user.password):
        data = {"sub": form.email, "expiry": time() + 43200 }
        jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
        response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)
        return {"token": jwt_token, "user": form.email, "message":"Login Successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Please Enter Email and Password"
        )


