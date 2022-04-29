from db_config.database import Base
from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)


class Profile_Pic(Base):
    __tablename__ = 'profile_pic'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    photo = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))


class OTP(Base):
    __tablename__='otp'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    otp = Column(String, nullable=False)
    status = Column(Boolean, default=False)
    exp_time = Column(Float, nullable=False)
    count_otp = Column(Integer, nullable=False)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    d_price = Column(Float, nullable=False)
    size = Column(String, nullable=False)
    category = Column(String, nullable=False)
    shop_id = Column(String, ForeignKey('users.id'))
    images = Column(String)


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key = True, index=True)
    product_name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    d_price = Column(Float, nullable=False)
    size = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'))
    user_id = Column(Integer, ForeignKey('users.id'))