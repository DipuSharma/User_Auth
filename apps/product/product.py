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
from datetime import datetime
from importlib.metadata import files
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import desc, or_
from hash_model.schemas import CreateProduct, SearchProduct
from hash_model.models import Product, User
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db_config.database import get_db
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from apps.auth.login import oauth2_scheme
from jose import jwt
from db_config.config import setting
from pathlib import Path


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent


@router.post('/add-product', tags=['Product'])
async def create_emp(p_name: str = Form(...), description: str = Form(...), price: str = Form(...), d_price: str = Form(...), size: str = Form(...), categ: str = Form(...),
                     file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    ext = os.path.splitext(file.filename)
    IMG_DIR = './static/pro_image/'
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(
            status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join(IMG_DIR, file_name), mode='wb') as f:
        await f.write(content)
    if token:
        verified = jwt.decode(token, setting.SECRET_KEY,
                              algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            user = db.query(User).filter(User.email == verified['sub'] and User.type == verified['type']).first()
            print(user.id)
            e_name = db.query(Product).filter(and_(Product.shop_id == user.id, Product.product_name == p_name)).first()
            if not e_name:
                owner_id = user.id
                data = Product(product_name=p_name, description=description, price=price, d_price=d_price, size=size, category=categ,
                               shop_id=owner_id, images=file_name)
                db.add(data)
                db.commit()
                return {"status": "success", "message": "Item successfully created"}
            else:
                return {"status": "failed", "message": "The Product of This Name exists already", "data": e_name}
        else:
            return {"status": "failed", "message": "You are not authorized"}
    else:
        return {"status": "failed", "message": "Token Not Found"}

# Get User All Product


@router.get('/product/user/all', tags=['Product'])
async def all_product(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token:
        verified = jwt.decode(token, setting.SECRET_KEY,
                              algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            user = db.query(User).filter(User.email == verified['sub']).first()
            # result_by_auth_client = session.query(ClientTotal).filter(ClientTotal.client == auth_client_name).order_by(ClientTotal.id.desc()).all()
            items = db.query(Product).filter(
                Product.shop_id == user.id).order_by(Product.id.desc()).all()
            print(items)
            return {"status": "success", "message": "All data fetch successfully", "data": items}
        else:
            return {"status": "failed", "message": "token expire please re-login"}
    else:
        return {"status": "failed", "message": "Not Authenticated"}

# Product Advance Filter Api


@router.get("/product-search", tags=['Product'])
async def product_search(search: SearchProduct = Depends(),
                         db: Session = Depends(get_db),
                         token: str = Depends(oauth2_scheme)
                         ):
    payload = jwt.decode(token, setting.SECRET_KEY,
                         algorithms=setting.ALGORITHM)
    if payload['expiry'] >= time():
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        # if search:
        #     price_list = search.split(',')
        #     p_name = db.query(Product).filter(
        #         Product.price.in_([float(x) for x in price_list])).all()
        if search:
            print(dir(pdfkit))
            # if search.replace('.','',1).isdigit():
            #     x = search.split('.')
            #     data = (x[0] + x[1] + '.0')
            #     date_string = search
            #     print (datetime.fromisoformat(date_string))
            #     p_name = db.query(Product).filter(Product.price == data).all()
            try:
                if search.isdigit():
                    amt = int(search)*100
                    p_name = db.query(Product).filter(
                        Product.price == amt).all()
                if '-' in search:
                    print(search)
            except:
                pass
            p_name = db.query(Product).filter(or_(
                Product.product_name.ilike(f'%{search}%'),
                Product.category.ilike(f'%{search}%')
            )).all()
        return {"status": "Success", "message": "Your search item successfully", "data": p_name}
    else:
        return {"status": "success", "message": "You are not authorized"}

# Get All Product Api


@router.get('/product/all', tags=['Product'])
async def all_employee(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if token:
        verified = jwt.decode(token, setting.SECRET_KEY,
                              algorithms=setting.ALGORITHM)
        if verified['expiry'] >= time():
            # user = db.query(User).filter(User.email == verified['sub']).first()
            items = db.query(Product).order_by(Product.id.desc()).all()
            return {"status": "success", "message": "All data fetch successfully", "data": items}
        else:
            return {"status": "failed", "message": "token expire please re-login"}
    else:
        return {"status": "failed", "message": "Not Authenticated"}

# Get Singe Product


@router.get("/product", tags=['Product'])
async def product_fetch(id: int = Query(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, setting.SECRET_KEY,
                         algorithms=setting.ALGORITHM)
    if payload['expiry'] >= time():
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        item = db.query(Product).filter(Product.id == id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return {"status": "success", "message": "Single data fetch successfull", "data": item}
    else:
        return {"status": "failed", "message": "token expire please re-login"}

# Edit or Update Product


@router.put('/product/update', tags=['Product'])
async def product_edit(id: int = Query(default=None), item: CreateProduct = Body(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if item:
        payload = jwt.decode(token, setting.SECRET_KEY,
                             algorithms=setting.ALGORITHM)
        if payload['expiry'] >= time():
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
            existing_item = db.query(Product).filter(Product.id == id)
            if not existing_item.first():
                return {"message": f"No details found of {id} this id"}
            existing_item.update(jsonable_encoder(item))
            db.commit()
            return {"message": f"Details of id {id} Changed Successfully Update!!!"}
        else:
            return {"status": "failed", "message": "Token expire please re-login"}
    else:
        return {"status": "failed", "message": "All Field Required"}


# Delete Product
@router.delete('/product/delete', tags=['Product'])
async def delete_product(id: int = Query(default=None), db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, setting.SECRET_KEY,
                         algorithms=setting.ALGORITHM)
    if payload['expiry'] >= time():
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials.")
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
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
        return {"status": "failed", "message": "You are not authorized please re-login and try again"}


@router.post("/file/", tags=['File'])
async def create_upload_file(file: UploadFile = File(...)):
    File_DIR = './static/images/'
    if not os.path.exists(File_DIR):
        os.makedirs(File_DIR)
    file_name = File_DIR + file.filename
    with open(file_name,'wb+') as f:
        f.write(files.file.read())
        f.close()
    return {"filename": file.filename, "dir": file_name}


def itrfile():
    header = ['name', 'area', 'country_code2', 'country_code3']
    data = ['Afghanistan', 652090, 'AF', 'AFG']
    with open('static/sample.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        writer.writerow(data)
        path_dir = os.getcwd()
        file_data = os.path.join(path_dir, "static/sample.csv")
        if os.path.exists(file_data):
            return file_data


@router.get('/export_data', tags=['Product'])
async def export_to_csv(db: Session = Depends(get_db)):
    if db:
        return FileResponse(itrfile(), media_type='csv')


@router.post('/csv-file', tags=['Product'])
async def generat_csv(db: Session = Depends(get_db)):
    # currency_query = db.query(Product).with_entities(Product.id, Product.product_name)

    # # Getting all the entries via SQLAlchemy
    # currencies = currency_query.all()
    items = db.query(Product).order_by(Product.id.desc()).all()
    df_from_records = pd.DataFrame([o.__dict__ for o in items])
    df = df_from_records.drop(['_sa_instance_state'], axis = 1)
    
    date = str(datetime.date(datetime.now()))
    date_format = date.replace('-', '')
    col = df.columns
    columns = [x.upper() for x in col]
    print(columns)
    stream = io.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]),media_type="text/csv")

    response.headers["Content-Disposition"] = f"attachment; filename={date}.csv"
    
    return response
