import os
from time import time
from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, UploadFile, status
from hash_model.schemas import CreateProduct
from hash_model.models import Product, User
from sqlalchemy.orm import Session
from db_config.database import get_db
from typing import List
from fastapi.encoders import jsonable_encoder
from routers.login import oauth2_scheme
from jose import jwt
from db_config.config import setting

router = APIRouter()


@router.post('/add-product', tags=['Product'])
async def create_emp(item: CreateProduct, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not item:
        return {"status": "failed", "message":"All Field required"}
    elif token:
        verified = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            user = db.query(User).filter(User.email == verified['sub']).first()
            e_name = db.query(Product).filter(Product.name == item.name).first()
            if not e_name:
                owner_id = user.id
                data = Product(name= item.name, description=item.description, price=item.price, d_price= item.d_price, photo= item.price, owner_id= owner_id)
                db.add(data)
                db.commit()
                return {"status":"success","message": "Item successfully created", "data": data}
            else:
                return {"status": "failed", "message": "The Product of This Name exists already", "data": e_name}
        else:
            return {"status":"failed", "message":"You are not authorized"}
    else:
        return {"status":"failed", "message":"Token Not Found"}



@router.get('/product/all', tags=['Product'])
async def all_employee(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token:
        verified = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            items = db.query(Product).all()
            return {"status": "success", "message": "All data fetch successfully", "data":items}
        else:
            return {"status":"failed", "message":"token expire please re-login"}


@router.get("/product", tags=['Product'])
async def employee_fetch(id: int = Query(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
    if payload['expiry'] >= time():
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        item = db.query(Product).filter(Product.id == id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return {"status":"success", "message":"Single data fetch successfull", "data":item}
    else:
        return {"status":"failed", "message":"token expire please re-login"}



@router.put('/product/update', tags=['Product'])
async def employee_edit(id: int = Query(default=None), item: CreateProduct = Body(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if item:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        if payload['expiry'] >= time():
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
            existing_item = db.query(Product).filter(Product.id == id)
            if not existing_item.first():
                return {"message": f"No details found of {id} this id"}
            existing_item.update(jsonable_encoder(item))
            db.commit()
            return {"message": f"Details of id {id} Changed Successfully Update!!!"}
        else:
            return {"status":"failed", "message":"Token expire please re-login"}
    else:
        return {"status": "failed", "message": "All Field Required"}


@router.delete('/product/delete', tags=['Product'])
async def delete_employee(id: int = Query(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
    if payload['expiry'] >= time():
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials.")
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        existing_item = db.query(Product).filter(Product.id == id)
        if not existing_item.first():
            return {"message": f"No details found of item Id {id}"}
        if existing_item.first().owner_id == user.id:
            existing_item.delete()
            db.commit()
            return {"message": f"Item id {id} has been successfully deleted"}
        else:
            return {"message": "You are Not Authorized"}
    else:
        return {"status":"failed", "message":"You are not authorized please re-login and try again"}

@router.post("/create_file", tags=["File"])
async def image_upload(image: UploadFile = File(default=None)):
    try:
        os.mkdir("static/images")
    except Exception as e: 
        file_name = os.getcwd()+"/static/images/"+image.filename.replace(" ", "-")
        with open(file_name,'wb+') as f:
            f.write(image.file.read())
            f.close()
        file = jsonable_encoder({"imagePath":file_name})
        # new_image = await add_image(file)
        return {"filename": file_name}       