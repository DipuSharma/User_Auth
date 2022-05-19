from time import time
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from jose import jwt
from db_config.config import setting
from db_config.database import get_db
from apps.auth.login import oauth2_scheme
from hash_model.models import Address, User
from sqlalchemy.orm import join

router = APIRouter()


@router.post('/shop-details', tags=['Shop'])
async def get_list(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="you are unauthorized")
    verified = jwt.decode(token, setting.SECRET_KEY,algorithms=setting.ALGORITHM)
    if verified['expiry'] >= time():
        user = db.query(User).filter(User.email == verified['sub'] and User.type == verified['type']).first()
        data = db.query(User).join(Address).filter(Address.user_id == user.id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Address not found of this user")
        print(data.address)
        return {"status":"success", "data":data}
    else:
        return {"status": "failed", "message": "You are not authorized"}
        
   