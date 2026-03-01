from sqlalchemy import Column, Integer, String, Enum, ForeignKey,DateTime
from Database.database import Base
from Enum.complaint_type import ComplainTypes_Enum
from Enum.category_enum import Category_Enum
from Enum.status_enum import Status_Enum
from sqlalchemy.sql import func

class ComplainModel(Base):
    __tablename__="complain"

    complain_id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    complain_type=Column(Enum(ComplainTypes_Enum),nullable=False)
    category=Column(Enum(Category_Enum),default=Category_Enum.Minor,nullable=False)
    description=Column(String,nullable=False)
    location=Column(String,nullable=False)
    status=Column(Enum(Status_Enum),default=Status_Enum.Pending,nullable=False)

    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())
    created_at=Column(DateTime,server_default=func.now())

