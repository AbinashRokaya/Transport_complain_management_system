from fastapi import APIRouter,Depends,HTTPException,status
from Schema.complain_schema import ComplainRequest,StatusUpdate,ComplainResponse,ComplainListResponse
from Database.database import db_dependancy
from Model.complain_model import ComplainModel
from Model.register_model import RegisterModel
from Model.department_model import DepartmentModel
from Model.branch_model import BranchModel
from typing import Annotated
from Auth.get_current_user import require_permission
from sqlalchemy import and_,or_
from Enum.complaint_type import ROAD_TYPES,TRANSPORT_TYPES

route=APIRouter(
    prefix="/api/complain",
    tags=["complain"]
)
categories = ["Minor", "Moderate", "Severe", "Emergency"]
@route.post("/post",status_code=201)
def complain_create(request:ComplainRequest,db:db_dependancy,current_user=Depends(require_permission("view"))):
    try:
        user=db.query(RegisterModel).filter(RegisterModel.name==current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=409,detail=f"user email {current_user.username} alredy exist")
        
        if request.complain_type in ROAD_TYPES:
            department_type="Road"
        if request.complain_type in TRANSPORT_TYPES:
            department_type="Transport"




        
    
        new_complain=ComplainModel(
            user_id=user.id,
            department=department_type,
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
    
@route.get("/{status}/{category}", status_code=200)
def get_all_complains(status:str,category:str,db: db_dependancy, current_user=Depends(require_permission("view"))):
    try:
        
        query = db.query(ComplainModel)

        if status != "All":
            query = query.filter(ComplainModel.status == status)

        if category != "All":
            query = query.filter(ComplainModel.category == category)

        complains = query.all()
        if not complains:
            raise HTTPException(status_code=404, detail=f"Complain not found")

        complains=[ComplainResponse(
            complain_id=complain.complain_id,
            complain_type=complain.complain_type,
            department=complain.department,
            status=complain.status,
            category=complain.category,
            description=complain.description,
            location=complain.location,
            created_at=complain.created_at,
            update_at=complain.update_at,
            user_name=complain.user.name



        )for complain in complains]


        
        return {"complains": ComplainListResponse(complains=complains)}
    except Exception as e:

        raise HTTPException(status_code=500,detail=f"{e}")
    
@route.get("/{status}", status_code=200)
def get_all_complains(status:str,db: db_dependancy, current_user=Depends(require_permission("view"))):
    try:
        user=db.query(RegisterModel).filter(RegisterModel.name==current_user["username"]).first()
        department=db.query(DepartmentModel).filter(DepartmentModel.user_id==user.id).first()
        branch=db.query(BranchModel).filter(BranchModel.department_id==department.department_id).first()
        query = db.query(ComplainModel).filter(
    ComplainModel.location == branch.branch_name
)
        query=db.query(ComplainModel).filter(ComplainModel.department==department.department_name)

        if status != "All":
            query = query.filter(ComplainModel.status == status)


        complains = query.all()
        if not complains:
            raise HTTPException(status_code=404, detail=f"Complain not found")
        complains=[ComplainResponse(
            complain_id=complain.complain_id,
            complain_type=complain.complain_type,
            department=complain.department,
            status=complain.status,
            category=complain.category,
            description=complain.description,
            location=complain.location,
            created_at=complain.created_at,
            update_at=complain.update_at,
            user_name=complain.user.name



        )for complain in complains]


        
        return {"complains": ComplainListResponse(complains=complains)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
# @route.get("/Pending", status_code=200)
# def get_all_complains(db: db_dependancy, current_user=Depends(require_permission("view"))):
#     try:
#         complains = db.query(ComplainModel).filter(ComplainModel.status=="Pending").all()
#         if not complains:
#             raise HTTPException(status_code=404, detail=f"Pending Complain not found")
#         return {"complains": complains}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"{e}")
    
# @route.get("/In_Progress", status_code=200)
# def get_all_complains(db: db_dependancy, current_user=Depends(require_permission("view"))):
#     try:
#         complains = db.query(ComplainModel).filter(ComplainModel.status=="In_Progress").all()
#         if not complains:
#             raise HTTPException(status_code=404, detail=f"In Progress Complain not found")
#         return {"complains": complains}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"{e}")
    
# @route.get("/Resolved", status_code=200)
# def get_all_complains(db: db_dependancy, current_user=Depends(require_permission("view"))):
#     try:
#         complains = db.query(ComplainModel).filter(ComplainModel.status=="Resolved").all()
#         if not complains:
#             raise HTTPException(status_code=404, detail=f"Resolved Complain not found")
#         return {"complains": complains}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"{e}")
    
@route.get("/{complain_id}", status_code=200)
def get_complain(complain_id: int, db: db_dependancy, current_user=Depends(require_permission("view"))):
    complain = db.query(ComplainModel).filter(ComplainModel.complain_id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail=f"Complain with id {complain_id} not found")
    return {"complain": complain}


@route.put("/status/{complain_id}", status_code=200)
def update_complain(complain_id: int, status:StatusUpdate, db: db_dependancy, current_user=Depends(require_permission("view"))):
    complain = db.query(ComplainModel).filter(ComplainModel.complain_id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail=f"Complain with id {complain_id} not found")


    complain.status = status.status

    db.commit()
    db.refresh(complain)
    return {"msg": "Complain updated successfully", "updated_complain": complain}

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