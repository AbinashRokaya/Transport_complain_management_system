from sqlalchemy import Column, Integer, String, Enum, ForeignKey,DateTime
from Database.database import Base
from Enum.complaint_type import ComplainTypes_Enum
from Enum.category_enum import Category_Enum
from Enum.status_enum import Status_Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class BranchModel(Base):
    __tablename__="branch"

    branch_id=Column(Integer,primary_key=True,index=True)
    department_id=Column(Integer,ForeignKey("department.department_id",ondelete="CASCADE"),nullable=False)
    branch_name=Column(String,nullable=False)
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())
    created_at=Column(DateTime,server_default=func.now())


    department=relationship("DepartmentModel",back_populates="branch")

