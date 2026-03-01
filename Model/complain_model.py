from sqlalchemy import Column, Integer, String, Enum, ForeignKey,DateTime
from Database.database import Base
from Enum.complaint_type import ComplainTypes_Enum
from sqlalchemy.sql import func

class ComplainModel(Base):
    complain_id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("register.id",ondelete="CASCADE"))
    complain_type=Column(Enum(ComplainTypes_Enum))
    category=Column()
    description=Column(String)
    location=Column(String)
    status=Column()

    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())
    created_at=Column(DateTime,server_default=func.now())

