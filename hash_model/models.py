from numpy import product
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
    address = relationship("Address", back_populates="users")

class ShopKeeper(Base):
    __tablename__ = 'shopkeeper'
    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=True)
    register_no = Column(String, nullable=True)
    mobile_no = Column(String, nullable=True)
    email_id = Column(String, nullable=True)
    gst_no = Column(String, nullable=True)
    address_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    product = relationship("Product", back_populates="users")
    
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    address_line_1 = Column(String, nullable=True)
    address_line_2 = Column(String, nullable=True)
    country_name = Column(String, nullable=True)
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    zipcode = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shop_id = Column(Integer, ForeignKey("shopkeeper.id"))
    user = relationship("User", back_populates="address")
    shopkeeper = relationship("ShopKeeper", back_populates="address")


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
    shopkeeper_id = Column(Integer, ForeignKey("shopkeeper.id"))
    product_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    d_price = Column(Float, nullable=False)
    size = Column(String, nullable=False)
    category = Column(String, nullable=False)
    shop_id = Column(String, ForeignKey('users.id'))
    images = Column(String)

    shopkeeper = relationship("ShopKeeper", back_populates="product")

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