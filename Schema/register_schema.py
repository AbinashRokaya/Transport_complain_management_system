from pydantic import BaseModel,EmailStr,field_validator
import re

class RegisterRequest(BaseModel):
    number:str=None
    name:str=None
    address:str
    email:EmailStr
    password:str

    @field_validator("number")
    @classmethod
    def validate_number(cls, value):
        pattern = r"^9[78]\d{8}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid Nepal phone number")
        return value