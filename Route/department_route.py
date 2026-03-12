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

@route.post("/post", status_code=201, response_model=DepartmentResponse)
def department_create(
    request: DepartmentRequest,
    db: db_dependancy,
    current_user=Depends(require_permission("view"))
):
    try:
       
        user = db.query(RegisterModel).filter(RegisterModel.id == request.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        department = db.query(DepartmentModel).filter(
            DepartmentModel.user_id == user.id
        ).first()

        branch = db.query(BranchModel).filter(
            BranchModel.department_id == department.department_id
        ).first() if department else None

        
        if request.department_name:
            department = db.query(DepartmentModel).filter(
                DepartmentModel.user_id == user.id
            ).first()

            if department:
                department.department_name = request.department_name
            else:
                department = DepartmentModel(
                    user_id=user.id,
                    department_name=request.department_name
                )
                db.add(department)

            db.commit()
            db.refresh(department)

           
            if request.branch_name:
                branch = db.query(BranchModel).filter(
                    BranchModel.department_id == department.department_id
                ).first()

                if branch:
                    branch.branch_name = request.branch_name
                else:
                    branch = BranchModel(
                        branch_name=request.branch_name,
                        department_id=department.department_id
                    )
                    db.add(branch)

                db.commit()
                db.refresh(branch)

       
        if request.role:
            user.role = request.role
            db.commit()
            db.refresh(user)

        # 5. Build and return response
        return DepartmentResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            address=user.address,
            number=user.number,
            department_name=department.department_name if department else None,
            branch_name=branch.branch_name if branch else None,
            role=user.role
        )

    except HTTPException:
        raise  # re-raise 404 cleanly, don't swallow it as 500
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
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
    


    
