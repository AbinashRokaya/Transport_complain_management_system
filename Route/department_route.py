from fastapi import APIRouter,Depends,HTTPException,status
from Schema.complain_schema import ComplainRequest,StatusUpdate,ComplainResponse,ComplainListResponse
from Database.database import db_dependancy
from Model.branch_model import BranchModel
from Model.register_model import RegisterModel
from Model.department_model import DepartmentModel
from typing import Annotated
from Auth.get_current_user import require_permission
from sqlalchemy import and_,or_
from Schema.department_schema import DepartmentRequest,DepartmentResponse,DepartmentListResponse

route=APIRouter(
    prefix="/api/department",
    tags=["department"]
)

@route.post("/post",status_code=201)
def department_create(request:DepartmentRequest,db:db_dependancy,current_user=Depends(require_permission("view"))):
    try:
        user=db.query(RegisterModel).filter(RegisterModel.id==request.id).first()
        if not user:
            raise HTTPException(status_code=404,detail="user not found")
        

        new_department=DepartmentModel(
            user_id=user.id,
            department_name=request.department_name    
        )
        db.add(new_department)
        db.commit()
        db.refresh(new_department)

        new_branch=BranchModel(
            branch_name=request.branch_name,
            department_id=new_department.department_id

        )
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)

        user.role=request.role
        db.commit()
        db.refresh(user)
        
        return {"msg":"department admin successfully added","department":new_department}
        

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
@route.get("/{status}",status_code=200)
def get_all_user(status:str,db: db_dependancy, current_user=Depends(require_permission("view"))):
    query=db.query(RegisterModel)
    if status!="All":
         query=query.filter(RegisterModel.address==status)
    users=query.all()
    if not users:
            raise HTTPException(status_code=404,detail="user not found")
    all_user=[DepartmentResponse(
         department_name=i.department.department_name if i.department else None,
         branch_name=i.department.branch.branch_name if i.department else None,
         name=i.name,
         address=i.address,
         email=i.email,
         roll=i.role,
         id=i.id
         
    )for i in users]

    return {"users":DepartmentListResponse(user=all_user)}
    


    
