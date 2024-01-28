from typing import List, Optional
from datetime import datetime
import polars as pl 
from sqlalchemy import insert
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            )
from sqlalchemy.types import Float, String,Integer,Date,Text

mysql_uri = 'mysql+mysqlconnector://root:mysql@localhost:3307/divistant'

mysql = create_engine(mysql_uri,echo = True )

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = 'Orders'
    
    id= mapped_column(Integer,primary_key=True,autoincrement = True)
    CreatedAt: Mapped[datetime] = mapped_column(Date)
    Users : Mapped[int]
    ProductName : Mapped[Optional[str]] = mapped_column(String(25))
    Price : Mapped[Optional[float]] = mapped_column(Float(decimal_return_scale = 1))
    Quantity : Mapped[Optional[float]] = mapped_column(Float(decimal_return_scale = 1))
    TotalPrice : Mapped[Optional[float]]= mapped_column(Float(decimal_return_scale = 1))
    
class OrderId(Base):
    __tablename__ = 'OrdersId'
    
    id : Mapped[int] = mapped_column(primary_key = True,
                                     autoincrement = False)
    Name : Mapped[str] = mapped_column(String(25))
    Gender :Mapped[str] = mapped_column(String(10))
    Address : Mapped[Optional[str]] = mapped_column(String(50))
    
Base.metadata.create_all(mysql)

order_dict = pl.read_csv('order.csv').to_dicts()
orderid_dict = pl.read_csv('orderid.csv').to_dicts()

with mysql.connect() as conn:
    conn.execute(insert(OrderId),orderid_dict)
    conn.execute(insert(Order),order_dict)
    conn.commit()