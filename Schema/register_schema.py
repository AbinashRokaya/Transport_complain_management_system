from pydantic import BaseModel,EmailStr

class RegisterRequest(BaseModel):
    name:str=None
    address:str
    email:EmailStr
    password:str
