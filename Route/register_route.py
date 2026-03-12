from fastapi import APIRouter,Depends,HTTPException,status
from Schema.register_schema import RegisterRequest
from Database.database import db_dependancy
from Model.register_model import RegisterModel
from Auth.hash_password import hash_password_user


route=APIRouter(
    prefix=("/api"),
    tags=['register']
)

@route.post("/register",status_code=201)
def register_user(user:RegisterRequest,db:db_dependancy):
    try:
        exist_email=db.query(RegisterModel).filter(RegisterModel.email==user.email).first()

        if exist_email:
            raise HTTPException(status_code=409,detail=f"{user.email} already exist")
        
        hash_pasword=hash_password_user(user.password)

        new_user=RegisterModel(
            number=user.number,
            name=user.name,
            address=user.address,
            email=user.email,
            password=hash_pasword
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"msg":"Successfully created new user"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")

        


        



