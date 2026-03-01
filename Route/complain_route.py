from fastapi import APIRouter,Depends,HTTPException,status
from Schema.complain_schema import ComplainRequest
from Database.database import db_dependancy
from Model.complain_model import ComplainModel
from Model.register_model import RegisterModel
from typing import Annotated
from Auth.get_current_user import require_permission

route=APIRouter(
    prefix="/api/complain",
    tags=["complain"]
)

@route.post("/update",status_code=201)
def complain_create(request:ComplainRequest,db:db_dependancy,current_user=Depends(require_permission("view"))):
    try:
        user=db.query(RegisterModel).filter(RegisterModel.name==current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=409,detail=f"user email {current_user.username} alredy exist")
    
        new_complain=ComplainModel(
            user_id=user.id,
            complain_type=request.complain_type,
            category=request.category,
            description=request.description,
            location=request.location,
        
            
        )
        db.add(new_complain)
        db.commit()
        db.refresh(new_complain)

        return {"msg":"add new complain","new_post":new_complain}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
@route.get("/", status_code=200)
def get_all_complains(db: db_dependancy, current_user=Depends(require_permission("view"))):
    try:
        complains = db.query(ComplainModel).all()
        return {"complains": complains}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
@route.get("/{complain_id}", status_code=200)
def get_complain(complain_id: int, db: db_dependancy, current_user=Depends(require_permission("view"))):
    complain = db.query(ComplainModel).filter(ComplainModel.complain_id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail=f"Complain with id {complain_id} not found")
    return {"complain": complain}


@route.put("/{complain_id}", status_code=200)
def update_complain(complain_id: int, request: ComplainRequest, db: db_dependancy, current_user=Depends(require_permission("view"))):
    complain = db.query(ComplainModel).filter(ComplainModel.complain_id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail=f"Complain with id {complain_id} not found")

    
    user = db.query(RegisterModel).filter(RegisterModel.name == current_user["username"]).first()
    if not user or complain.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this complain")

    complain.complain_type = request.complain_type
    complain.category     = request.category
    complain.description  = request.description
    complain.location     = request.location

    db.commit()
    db.refresh(complain)
    return {"msg": "Complain updated successfully", "updated_complain": complain}

@route.delete("/{complain_id}", status_code=200)
def delete_complain(complain_id: int, db: db_dependancy, current_user=Depends(require_permission("view"))):
    complain = db.query(ComplainModel).filter(ComplainModel.complain_id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail=f"Complain with id {complain_id} not found")

   
    user = db.query(RegisterModel).filter(RegisterModel.name == current_user["username"]).first()
    if not user or complain.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this complain")

    db.delete(complain)
    db.commit()
    return {"msg": f"Complain with id {complain_id} deleted successfully"}