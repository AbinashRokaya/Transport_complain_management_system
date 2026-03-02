from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from Database.database import Base
from sqlalchemy.sql import func

class BranchModel(Base):
    __tablename__ = "branch"

    branch_id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("department.department_id", ondelete="CASCADE"), nullable=False)
    branch_name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
