from fastapi import APIRouter,Depends,HTTPException,status
from Schema.complain_schema import ComplainRequest,StatusUpdate,ComplainResponse,ComplainListResponse
from Database.database import db_dependancy
from Model.branch_model import BranchModel
from Model.department_model import DepartmentModel
from typing import Annotated
from Auth.get_current_user import require_permission
from sqlalchemy import and_,or_

route=APIRouter(
    prefix="/api/branch",
    tags=["branch"]
)
