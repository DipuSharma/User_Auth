from unicodedata import category
from db_config.database import Base
from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey, true
from sqlalchemy.orm import relationship




class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    first = relationship("Product", back_populates="second")


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    d_price = Column(Float, nullable=False)
    photo = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    second = relationship("User", back_populates="first")