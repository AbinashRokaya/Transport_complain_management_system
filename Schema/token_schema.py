from pydantic import BaseModel,EmailStr


class TokenRequest(BaseModel):
    name:str
    email:EmailStr
    