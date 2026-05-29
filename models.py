
#! TODO: 
#? Implement Alembic for version control of DB changes 
# ? postgres in docker 
# ? get the url from .env not directly 

from sqlalchemy import create_engine, String,ForeignKey
from dotenv  import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database import Base ,engine


# an example mapping using the base
class User(Base):
    __tablename__='users'
    id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(unique=True, nullable=False)
    password:Mapped[str]=mapped_column(nullable=False)


class Stock(Base):
    __tablename__='stocks'
    id:Mapped[int]=mapped_column(primary_key=True) # checck if its a foreign key or not ??? 
    title:Mapped[str]=mapped_column()
    symbol:Mapped[str]=mapped_column()


class Order(Base):
    __tablename__='orders'
    id:Mapped[int]=mapped_column(primary_key=True) # checck if its a foreign key or not ??? 
    userId:Mapped[int]=mapped_column(ForeignKey('users.id'))
    side:Mapped[str]=mapped_column()
    type:Mapped[str]=mapped_column()
    stockId:Mapped[int]=mapped_column(ForeignKey('stocks.id'))
    price:Mapped[int]=mapped_column()
    qty:Mapped[int]=mapped_column()
    filled_qty:Mapped[int]=mapped_column()
    status:Mapped[str]=mapped_column()

class Fill(Base):
    __tablename__='fills'
    id:Mapped[int]=mapped_column(primary_key=True) 
    stockId:Mapped[int]=mapped_column(ForeignKey('stocks.id'))
    price:Mapped[int]=mapped_column()
    qty:Mapped[int]=mapped_column()
    buyOrderId:Mapped[int]=mapped_column(ForeignKey("orders.id"))
    selOrderId:Mapped[int]=mapped_column(ForeignKey("orders.id"))



# Creating the Tables 
Base.metadata.create_all(engine) 

# 'User' is python class , we name it anything like Apple
# 'user' this is the actual table name inside the PostgreSQL , it exists inside the db
# when to use  "side: Mapped[str]" and when to use "email   = Column(String, unique=True)" refer Syntax Wala doc


