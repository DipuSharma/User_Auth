from email.policy import default
from numpy import product
from db_config.database import Base, engine
from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship


addresss_users= Table('address_users', Base.metadata,
    Column('users_id', ForeignKey('users.id'), primary_key=True),
    Column('address_id', ForeignKey('address.id'), primary_key=True)
    
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    type = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    address = relationship("Address", secondary=addresss_users, back_populates="users")

    
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=True)
    register_number = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    mobile_number = Column(String, nullable=False)
    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    zipcode = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", secondary=addresss_users,back_populates = 'address')


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
    images = Column(String)
    shop_id = Column(Integer, ForeignKey("users.id"))

    # shopkeeper = relationship("ShopKeeper", secondary="product_shopkeeper" ,back_populates="product")

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

Base.metadata.create_all(engine)