from sqlalchemy import Column, Integer, String, DateTime
from Database.database import Base
from sqlalchemy.sql import func

class DepartmentModel(Base):
    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String, nullable=False, unique=True)
    department_code = Column(String, nullable=False, unique=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
