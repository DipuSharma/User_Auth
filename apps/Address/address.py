
from operator import and_
import os
import io
import csv
import uuid
import pdfkit
import aiofiles
import pandas as pd
from time import time
from glob import glob
from importlib.metadata import files
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import desc, or_
from hash_model.schemas import AddressCreate
from hash_model.models import Address, User
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db_config.database import get_db
from apps.auth.login import oauth2_scheme
from jose import jwt
from db_config.config import setting

router = APIRouter()


@router.post('/add-address', tags=['User'])
async def add_address(address: AddressCreate = Body(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="You are not authorized")
    verified = jwt.decode(token, setting.SECRET_KEY,algorithms=setting.ALGORITHM)
    if not verified['expiry'] >= time():
        raise HTTPException(status_code=402, detail="You are not authorized")
    user = db.query(User).filter(User.email == verified['sub'] and User.type == verified['type']).first()
    if not user:
        raise HTTPException(status_code=401, detail="You are Unauthorized")
    user_address = db.query(Address).filter(Address.user_id == user.id).first()
    if not user_address:
        try:
            owner_id = user.id
            data = Address(shop_name=address.shop_name, register_number=address.register_number, gst_number=address.gst_number, mobile_number=address.mobile_number,
                        address_line_1=address.address_line_1, address_line_2=address.address_line_2,
                                country_name=address.country_name, state=address.state, district=address.district, zipcode=address.zipcode, user_id=owner_id)
            user.address.append(data)
            db.commit()
            return {"status":"success", "message":"address add successfully"}
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Address not add {e}")
    
    else:
        return {"status":"failed", "message":"Address already exists"}
        
                
