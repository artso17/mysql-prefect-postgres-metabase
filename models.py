
# Import all neccessary libraries
from typing import Optional
from datetime import datetime
import polars as pl 
from sqlalchemy import insert,select,func
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            )
from sqlalchemy.types import Float, String,Integer,Date

# Define mysql engine
mysql_uri = 'mysql+mysqlconnector://root:mysql@localhost:3307/divistant'
mysql = create_engine(mysql_uri,echo = True )

# Create Base model as parent model of all models
class Base(DeclarativeBase):
    pass

# Create source models
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
    
# Create tables based on given models
Base.metadata.create_all(mysql)

# Read dummy data and convert to dict data type
order_dict = pl.read_csv('order.csv').to_dicts()
orderid_dict = pl.read_csv('orderid.csv').to_dicts()

# Generate query to gather data of users who have more than 250 transactions
query = select(OrderId.Name, func.count(OrderId.Name))\
    .join(Order,OrderId.id == Order.Users)\
        .group_by(OrderId.Name)\
            .having(func.count(OrderId.Name) > 250)

# Print compiled script
print(query)

# Open connection to source database
with mysql.connect() as conn:
    # Insert all dummies data to source database
    # conn.execute(insert(OrderId),orderid_dict)
    # conn.execute(insert(Order),order_dict)
    # conn.commit()
    
    # Print the result of query script
    print(conn.execute(query).all())