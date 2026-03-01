from fastapi import APIRouter,Depends,HTTPException,status,Response
from Schema.login_schema import LoginRequest
from Database.database import db_dependancy
from Model.register_model import RegisterModel
from Auth.hash_password import verify_password
from Auth.jwt_token import create_access_token
from Schema.token_schema import TokenRequest


route=APIRouter(
    prefix=("/api"),
    tags=['login']
)

@route.post("/login",status_code=200)
def login_user(user:LoginRequest,db:db_dependancy,response:Response):
    try:
        exist_user=db.query(RegisterModel).filter(RegisterModel.name==user.name).first()

        if not exist_user:
            raise HTTPException(status_code=404,detail=f"{user.name} not found")

        if not verify_password(user.password,exist_user.password):
            raise HTTPException(status_code=400,detail="password is incorrect")
        token=TokenRequest(
            name=exist_user.name,
            email=exist_user.email,
            role=exist_user.role
        )

        access_token=create_access_token(token)
        response.set_cookie(
            key="access_token", 
                value=access_token, 
                httponly=True,   
                max_age=3600,    
                samesite="none",   # change from "lax" to "none" for cross-origin
                secure=True,       # Keep false for HTTP local dev
                path="/",       
        )
        user_detail={
            "name":exist_user.name,
            "email":exist_user.email,
            "address":exist_user.address,
            "role":exist_user.role
        }

        return {"msg":"login sucessfully","access_token":access_token,"user_detail":user_detail}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")





