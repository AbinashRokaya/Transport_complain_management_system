from pydantic import BaseModel,EmailStr
from Enum.department_enum import Department_Enum
from Schema.role_schema import Role_Schema
from typing import List,Optional

class DepartmentRequest(BaseModel):
    department_name:Optional[Department_Enum]=None
    branch_name:Optional[str]=None
    role:Optional[Role_Schema]=None
    id:int=None

class DepartmentResponse(BaseModel):
    department_name: Optional[Department_Enum] = None
    branch_name: Optional[str] = None
    number:int=None
    name:str=None
    address:str=None
    email:EmailStr=None
    roll:Role_Schema=None
    id:int=None
 

class DepartmentListResponse(BaseModel):
    user:List[DepartmentResponse]