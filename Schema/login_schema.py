from pydantic import BaseModel

class LoginRequest(BaseModel):
    name:str=None
    password:str=None