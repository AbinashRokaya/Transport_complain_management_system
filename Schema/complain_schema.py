from pydantic import BaseModel,EmailStr,field_serializer
from Enum.category_enum import Category_Enum
from Enum.complaint_type import ComplainTypes_Enum
from Enum.status_enum import Status_Enum
from typing import List
from datetime import datetime

class ComplainRequest(BaseModel):
    complain_type:ComplainTypes_Enum=None
    status:Status_Enum=Status_Enum.Pending
    category:Category_Enum=Category_Enum.Minor
    description:str=None
    location:str=None
    spefice_location:str=None
    cordinate_location:List[float]=None
    image_url:List[str]=None

class StatusUpdate(BaseModel):
    status: str

class ComplainResponse(BaseModel):
    complain_id:int=None
    complain_type:ComplainTypes_Enum=None
    department:str=None
    spefice_location:str=None
    cordinate_location:List[float]=None
    image_url:List[str]=None

    status:Status_Enum=Status_Enum.Pending
    category:Category_Enum=Category_Enum.Minor
    description:str=None
    location:str=None
    created_at:datetime=None
    update_at:datetime=None
    user_name:str

    @field_serializer('created_at', 'update_at')
    def serialize_dt(self, dt: datetime):
        return dt.date().isoformat()

class ComplainListResponse(BaseModel):
    complains:List[ComplainResponse]
class cordinateResponse(BaseModel):
    spefice_location:str=None
    cordinate_location:List[float]=None
    description:str=None
    user_name:str=None
    category:Category_Enum=None
class CordinateListResponse(BaseModel):
    cordinate:List[cordinateResponse]
