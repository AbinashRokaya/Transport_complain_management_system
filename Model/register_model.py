from sqlalchemy import Column,String,Integer,DateTime,Enum
from Database.database import Base
from sqlalchemy.sql import func
from Schema.role_schema import Role_Schema
from sqlalchemy.orm import relationship

class RegisterModel(Base):
    __tablename__="user"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role=Column(Enum(Role_Schema),default=Role_Schema.User)

    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())
    created_at=Column(DateTime,server_default=func.now())

    complaints = relationship(
        "ComplainModel",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    department = relationship(
        "DepartmentModel",
        back_populates="user",
        cascade="all, delete",
         uselist=False,
        passive_deletes=True
    )