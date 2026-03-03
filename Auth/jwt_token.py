import jwt
from jwt.exceptions import InvalidTokenError
import os
from Schema.token_schema import TokenRequest
from datetime import timedelta,datetime,timezone

SECRET_KEY = "67d7e6f89e3782b0510cf3cbcf2bb13cf76e180611cced825ab439701ee1d2a9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(subject: str,role: str,expires_delta:timedelta |None=None):
    to_encode={
    "sub":subject,
    
    "role":role
    }
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print(encode_jwt)
    return encode_jwt