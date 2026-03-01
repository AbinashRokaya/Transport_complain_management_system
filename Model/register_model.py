from sqlalchemy import Column,String,Integer,DateTime
from Database.database import Base
from sqlalchemy.sql import func

class RegisterModel(Base):
    __tablename__="user"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)

    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())
    created_at=Column(DateTime,server_default=func.now())

