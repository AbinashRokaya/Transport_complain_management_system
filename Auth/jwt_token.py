import jwt
from jwt.exceptions import InvalidTokenError
import os
from Schema.token_schema import TokenRequest
from datetime import timedelta,datetime,timezone

ACCESS_TOKEN_TIME=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def create_access_token(request:TokenRequest,expires_delta:timedelta |None=None):
    to_encode={
    "name":request.name,
    "email":request.email,
    "role":request.role
    }
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_TIME)

    to_encode.update({"exp":expire})
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM,)
    print(encode_jwt)
    return encode_jwt