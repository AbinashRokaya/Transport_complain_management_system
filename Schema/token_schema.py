from pydantic import BaseModel,EmailStr
from Schema.role_schema import Role_Schema


class TokenRequest(BaseModel):
    name:str
    email:EmailStr
    role:Role_Schema=Role_Schema.User
    