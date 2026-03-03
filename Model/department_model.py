from sqlalchemy import Column, Integer, String, Enum, ForeignKey,DateTime
from Database.database import Base
from Enum.complaint_type import ComplainTypes_Enum
from Enum.category_enum import Category_Enum
from Enum.status_enum import Status_Enum
from Enum.department_enum import Department_Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class DepartmentModel(Base):
    __tablename__="department"

    department_id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    department_name=Column(Enum(Department_Enum),nullable=False)
    update_at=Column(DateTime,server_default=func.now(),onupdate=func.now())
    created_at=Column(DateTime,server_default=func.now())

    user = relationship("RegisterModel", back_populates="department")


    branch = relationship(
        "BranchModel",
        back_populates="department",
        cascade="all, delete",
         uselist=False,
        passive_deletes=True
    )