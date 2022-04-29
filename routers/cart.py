from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import desc
from hash_model.schemas import CreateProduct
from hash_model.models import Product, User, Cart
from sqlalchemy.orm import Session
from db_config.database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from db_config.config import setting
from pathlib import Path
from time import time

router = APIRouter()

@router.post('/add-to-cart', tags=['Cart'])
async def create_cart(id: int = Query(default=None),db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
   payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
   if payload['expiry'] >= time():
      username = payload.get("sub")
      user = db.query(User).filter(User.email == username).first()
      item = db.query(Product).filter(Product.id == id).first()
      if not item:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
      qty = 1
      data = Cart(product_name=item.product_name, description=item.description, price=item.price, d_price=item.d_price, size=item.size, photo=item.images,
      category=item.category,quantity= qty, product_id=item.id, user_id= user.id)
      db.add(data)
      db.commit()
      return {"status":"success", "message": "You Item is in Cart"}
   else: return {"status":"failed", "message":"Session Expired"}
   

@router.put('/plus-item', tags=['Cart'])
async def plus_cart(id: int = Query(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
   if token:
      verified = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
      if verified['expiry'] >= time():
         email: str = verified.get("sub")
         user = db.query(User).filter(User.email == email).first()
         cart_item = db.query(Cart).filter(Cart.product_id == id and Cart.user_id == user.id).first()
         qty = cart_item.quantity + 1
         existing_data = db.query(Cart).filter(Cart.id == cart_item.id)
         existing_data.update({"quantity": qty})
         db.commit()
         return {"status": "success", "user_id":user.id, "item":qty}
      else:
         return {"status":"failed", "details":"Session Expired"}
   

@router.put('/minus-item', tags=['Cart'])
async def plus_cart(id: int = Query(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
   if token:
      verified = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
      if verified['expiry'] >= time():
         email: str = verified.get("sub")
         user = db.query(User).filter(User.email == email).first()
         cart_item = db.query(Cart).filter(Cart.product_id == id and Cart.user_id == user.id).first()
         qty = cart_item.quantity - 1
         if qty == 0:
            return {"status":"success", "details":"Quantity not allowed Zero, else this item deleted your cart"}
         existing_data = db.query(Cart).filter(Cart.id == cart_item.id)
         existing_data.update({"quantity": qty})
         db.commit()
         return {"status": "success", "user_id":user.id, "item":qty}
      else: return {"status":"failed", "details":"Session Expired"}