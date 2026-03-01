from pydantic import BaseModel,EmailStr
from Enum.category_enum import Category_Enum
from Enum.complaint_type import ComplainTypes_Enum
from Enum.status_enum import Status_Enum

class ComplainRequest(BaseModel):
    complain_type:ComplainTypes_Enum=None
    status:Status_Enum=Status_Enum.Pending
    category:Category_Enum=Category_Enum.Minor
    description:str
    location:str

