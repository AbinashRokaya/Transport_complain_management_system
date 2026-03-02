from sqlalchemy import Column, Integer, ForeignKey, DateTime
from Database.database import Base
from sqlalchemy.sql import func

class AssignmentModel(Base):
    __tablename__ = "assignment"

    assignment_id = Column(Integer, primary_key=True, index=True)
    complain_id = Column(Integer, ForeignKey("complain.complain_id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("department.department_id", ondelete="CASCADE"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branch.branch_id", ondelete="CASCADE"), nullable=False)
    
    assigned_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
