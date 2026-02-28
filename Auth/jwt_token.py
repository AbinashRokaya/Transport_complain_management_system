import jwt
from jwt.exceptions import InvalidTokenError
import os
from Schema.token_schema import TokenResponse
from datetime import timedelta,datetime,timezone

ACCESS_TOKEN_TIME=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def create_access_token(request:TokenResponse,expires_delta:timedelta |None=None):
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_TIME)

    request["exp"]=expire
    encode_jwt=jwt.encode(request,SECRET_KEY,algorithm=ALGORITHM,)
    print(encode_jwt)
    return encode_jwt