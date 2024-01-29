# Import all necessary libraries
from typing import List,Optional
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship
                            )
from sqlalchemy.types import Float, String,Integer,Date,Text

# Define Target postgres engine 
ps_uri = 'postgresql+psycopg2://postgres:postgres@localhost:5435/divistant'
ps_engine = create_engine(ps_uri,echo = True )

# Define Base model as parent of all models
class Base(DeclarativeBase):
    pass

# Define all target models
class Product(Base):
    """Product model stored ProductName from Order model and has relationship one-to-many
    """
    
    __tablename__ = 'products'
    
    id : Mapped[int] = mapped_column(primary_key = True,
                                     autoincrement = False)
    ProductName : Mapped[str] = mapped_column(String(25))
    
    orders: Mapped[List['Order']] = relationship(back_populates = 'products')
    
class User(Base):
    """User model is renamed model from OrderId model and it has relationship on-to-many with Order model.
    """
    
    __tablename__ = 'users'
    
    id : Mapped[int] = mapped_column(primary_key = True,
                                     autoincrement = False)
    Name : Mapped[str] = mapped_column(String(25))
    Gender :Mapped[str] = mapped_column(String(10))
    Address : Mapped[Optional[str]] = mapped_column(Text)
    
    orders : Mapped[List['Order']] = relationship(back_populates = 'users')


class Order(Base):
    """Order model is has 2 relationships such as User and Product
    """
    
    __tablename__ = 'orders'
    
    id= mapped_column(Integer,primary_key=True,autoincrement = True)
    CreatedAt: Mapped[datetime] = mapped_column(Date)
    UserId : Mapped[int] = mapped_column(ForeignKey('users.id'))
    Productid : Mapped[int] = mapped_column(ForeignKey('products.id'))
    Price : Mapped[Optional[float]] = mapped_column(Float(decimal_return_scale = 1))
    Quantity : Mapped[Optional[float]] = mapped_column(Float(decimal_return_scale = 1))
    TotalPrice : Mapped[Optional[float]]= mapped_column(Float(decimal_return_scale = 1))
    
    user: Mapped['User'] = relationship(back_populates = 'orders')
    product: Mapped['Product'] = relationship(back_populates = 'orders')


# Create tables based on defined models
Base.metadata.create_all(ps_engine)
