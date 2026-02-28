from pydantic import BaseModel,EmailStr


class TokenResponse(BaseModel):
    name:str
    email:EmailStr
    