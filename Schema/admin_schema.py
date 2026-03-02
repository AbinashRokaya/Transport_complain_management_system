from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Department Schemas
class DepartmentRequest(BaseModel):
    department_name: str
    department_code: str

class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    department_code: str
    created_at: datetime

    class Config:
        from_attributes = True


# Branch Schemas
class BranchRequest(BaseModel):
    department_id: int
    branch_name: str
    location: str

class BranchResponse(BaseModel):
    branch_id: int
    department_id: int
    branch_name: str
    location: str
    created_at: datetime

    class Config:
        from_attributes = True


# Assignment Schemas
class AssignmentRequest(BaseModel):
    complain_id: int
    department_id: int
    branch_id: int

class AssignmentResponse(BaseModel):
    assignment_id: int
    complain_id: int
    department_id: int
    branch_id: int
    assigned_at: datetime

    class Config:
        from_attributes = True


# Complaint Status Update Schema
class ComplaintStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None

class ComplaintWithAssignment(BaseModel):
    complain_id: int
    user_id: int
    complain_type: str
    category: str
    description: str
    location: str
    status: str
    created_at: datetime
    assignment: Optional[AssignmentResponse] = None

    class Config:
        from_attributes = True
