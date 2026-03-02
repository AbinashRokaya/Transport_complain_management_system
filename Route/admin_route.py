from fastapi import APIRouter, Depends, HTTPException, status
from Database.database import db_dependancy
from Model.complain_model import ComplainModel
from Model.register_model import RegisterModel
from Model.department_model import DepartmentModel
from Model.branch_model import BranchModel
from Model.assignment_model import AssignmentModel
from Schema.admin_schema import (
    DepartmentRequest, DepartmentResponse,
    BranchRequest, BranchResponse,
    AssignmentRequest, AssignmentResponse,
    ComplaintStatusUpdate, ComplaintWithAssignment
)
from Enum.status_enum import Status_Enum
from Auth.get_current_user import require_permission
from typing import List

route = APIRouter(
    prefix="/api/admin",
    tags=["admin"]
)


# ==================== DASHBOARD & STATISTICS ====================

@route.get("/dashboard", status_code=200)
def get_admin_dashboard(db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get admin dashboard with statistics"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        total_complaints = db.query(ComplainModel).count()
        pending_complaints = db.query(ComplainModel).filter(
            ComplainModel.status == Status_Enum.Pending
        ).count()
        in_progress_complaints = db.query(ComplainModel).filter(
            ComplainModel.status == Status_Enum.In_Progress
        ).count()
        resolved_complaints = db.query(ComplainModel).filter(
            ComplainModel.status == Status_Enum.Resolved
        ).count()
        
        total_departments = db.query(DepartmentModel).count()
        total_branches = db.query(BranchModel).count()
        
        return {
            "total_complaints": total_complaints,
            "pending": pending_complaints,
            "in_progress": in_progress_complaints,
            "resolved": resolved_complaints,
            "total_departments": total_departments,
            "total_branches": total_branches
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ==================== COMPLAINTS MANAGEMENT ====================

@route.get("/complaints", status_code=200)
def get_all_complaints(db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get all complaints (admin view)"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        complaints = db.query(ComplainModel).all()
        return {"complaints": complaints, "total": len(complaints)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/complaints/{complain_id}", status_code=200)
def get_complaint_details(complain_id: int, db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get specific complaint with assignment details"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        complaint = db.query(ComplainModel).filter(
            ComplainModel.complain_id == complain_id
        ).first()
        
        if not complaint:
            raise HTTPException(status_code=404, detail=f"Complaint with id {complain_id} not found")
        
        assignment = db.query(AssignmentModel).filter(
            AssignmentModel.complain_id == complain_id
        ).first()
        
        user = db.query(RegisterModel).filter(RegisterModel.id == complaint.user_id).first()
        
        return {
            "complaint": {
                "complain_id": complaint.complain_id,
                "user": {"name": user.name, "email": user.email} if user else None,
                "complain_type": complaint.complain_type.value,
                "category": complaint.category.value,
                "description": complaint.description,
                "location": complaint.location,
                "status": complaint.status.value,
                "created_at": complaint.created_at
            },
            "assignment": assignment
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.put("/complaints/{complain_id}/status", status_code=200)
def update_complaint_status(
    complain_id: int,
    request: ComplaintStatusUpdate,
    db: db_dependancy,
    current_user=Depends(require_permission("edit"))
):
    """Update complaint status"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can update complaint status")
        
        complaint = db.query(ComplainModel).filter(
            ComplainModel.complain_id == complain_id
        ).first()
        
        if not complaint:
            raise HTTPException(status_code=404, detail=f"Complaint with id {complain_id} not found")
        
        # Validate status
        try:
            new_status = Status_Enum(request.status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")
        
        complaint.status = new_status
        db.commit()
        db.refresh(complaint)
        
        return {
            "msg": "Complaint status updated successfully",
            "complaint": {
                "complain_id": complaint.complain_id,
                "status": complaint.status.value,
                "updated_at": complaint.update_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/complaints/status/{status}", status_code=200)
def get_complaints_by_status(status: str, db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get all complaints by status"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        try:
            status_enum = Status_Enum(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        complaints = db.query(ComplainModel).filter(
            ComplainModel.status == status_enum
        ).all()
        
        return {"status": status, "complaints": complaints, "total": len(complaints)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ==================== ASSIGNMENT MANAGEMENT ====================

@route.post("/complaints/{complain_id}/assign", status_code=201)
def assign_complaint_to_department(
    complain_id: int,
    request: AssignmentRequest,
    db: db_dependancy,
    current_user=Depends(require_permission("write"))
):
    """Assign complaint to a department and branch"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can assign complaints")
        
        # Verify complaint exists
        complaint = db.query(ComplainModel).filter(
            ComplainModel.complain_id == complain_id
        ).first()
        
        if not complaint:
            raise HTTPException(status_code=404, detail=f"Complaint with id {complain_id} not found")
        
        # Verify department exists
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == request.department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {request.department_id} not found")
        
        # Verify branch exists and belongs to department
        branch = db.query(BranchModel).filter(
            BranchModel.branch_id == request.branch_id,
            BranchModel.department_id == request.department_id
        ).first()
        
        if not branch:
            raise HTTPException(status_code=404, detail=f"Branch with id {request.branch_id} not found in this department")
        
        # Check if assignment already exists
        existing_assignment = db.query(AssignmentModel).filter(
            AssignmentModel.complain_id == complain_id
        ).first()
        
        if existing_assignment:
            # Update existing assignment
            existing_assignment.department_id = request.department_id
            existing_assignment.branch_id = request.branch_id
            db.commit()
            db.refresh(existing_assignment)
            
            return {
                "msg": "Complaint assignment updated successfully",
                "assignment": existing_assignment
            }
        
        # Create new assignment
        new_assignment = AssignmentModel(
            complain_id=complain_id,
            department_id=request.department_id,
            branch_id=request.branch_id
        )
        
        # Update complaint status to In_Progress
        complaint.status = Status_Enum.In_Progress
        
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)
        
        return {
            "msg": "Complaint assigned successfully",
            "assignment": new_assignment
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/assignments/{complain_id}", status_code=200)
def get_assignment_details(complain_id: int, db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get assignment details for a specific complaint"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        assignment = db.query(AssignmentModel).filter(
            AssignmentModel.complain_id == complain_id
        ).first()
        
        if not assignment:
            raise HTTPException(status_code=404, detail=f"No assignment found for complaint {complain_id}")
        
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == assignment.department_id
        ).first()
        
        branch = db.query(BranchModel).filter(
            BranchModel.branch_id == assignment.branch_id
        ).first()
        
        return {
            "assignment": assignment,
            "department": {"id": department.department_id, "name": department.department_name} if department else None,
            "branch": {"id": branch.branch_id, "name": branch.branch_name, "location": branch.location} if branch else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.delete("/assignments/{complaint_id}", status_code=200)
def remove_assignment(complaint_id: int, db: db_dependancy, current_user=Depends(require_permission("delete"))):
    """Remove assignment from a complaint"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can delete assignments")
        
        assignment = db.query(AssignmentModel).filter(
            AssignmentModel.complain_id == complaint_id
        ).first()
        
        if not assignment:
            raise HTTPException(status_code=404, detail=f"No assignment found for complaint {complaint_id}")
        
        db.delete(assignment)
        db.commit()
        
        return {"msg": f"Assignment for complaint {complaint_id} removed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ==================== DEPARTMENT MANAGEMENT ====================

@route.post("/departments", status_code=201)
def create_department(
    request: DepartmentRequest,
    db: db_dependancy,
    current_user=Depends(require_permission("write"))
):
    """Create a new department"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can create departments")
        
        # Check if department already exists
        existing_dept = db.query(DepartmentModel).filter(
            DepartmentModel.department_code == request.department_code
        ).first()
        
        if existing_dept:
            raise HTTPException(status_code=409, detail=f"Department with code {request.department_code} already exists")
        
        new_department = DepartmentModel(
            department_name=request.department_name,
            department_code=request.department_code
        )
        
        db.add(new_department)
        db.commit()
        db.refresh(new_department)
        
        return {
            "msg": "Department created successfully",
            "department": new_department
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/departments", status_code=200)
def get_all_departments(db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get all departments"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        departments = db.query(DepartmentModel).all()
        return {"departments": departments, "total": len(departments)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/departments/{department_id}", status_code=200)
def get_department(department_id: int, db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get specific department"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {department_id} not found")
        
        return {"department": department}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.put("/departments/{department_id}", status_code=200)
def update_department(
    department_id: int,
    request: DepartmentRequest,
    db: db_dependancy,
    current_user=Depends(require_permission("edit"))
):
    """Update department details"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can update departments")
        
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {department_id} not found")
        
        department.department_name = request.department_name
        department.department_code = request.department_code
        
        db.commit()
        db.refresh(department)
        
        return {
            "msg": "Department updated successfully",
            "department": department
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.delete("/departments/{department_id}", status_code=200)
def delete_department(
    department_id: int,
    db: db_dependancy,
    current_user=Depends(require_permission("delete"))
):
    """Delete department (and associated branches)"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can delete departments")
        
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {department_id} not found")
        
        db.delete(department)
        db.commit()
        
        return {"msg": f"Department with id {department_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ==================== BRANCH MANAGEMENT ====================

@route.post("/branches", status_code=201)
def create_branch(
    request: BranchRequest,
    db: db_dependancy,
    current_user=Depends(require_permission("write"))
):
    """Create a new branch under a department"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can create branches")
        
        # Verify department exists
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == request.department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {request.department_id} not found")
        
        new_branch = BranchModel(
            department_id=request.department_id,
            branch_name=request.branch_name,
            location=request.location
        )
        
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        
        return {
            "msg": "Branch created successfully",
            "branch": new_branch
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/branches", status_code=200)
def get_all_branches(db: db_dependancy, current_user=Depends(require_permission("view"))):
    """Get all branches"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        branches = db.query(BranchModel).all()
        return {"branches": branches, "total": len(branches)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.get("/branches/department/{department_id}", status_code=200)
def get_branches_by_department(
    department_id: int,
    db: db_dependancy,
    current_user=Depends(require_permission("view"))
):
    """Get all branches for a specific department"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can access this endpoint")
        
        # Verify department exists
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {department_id} not found")
        
        branches = db.query(BranchModel).filter(
            BranchModel.department_id == department_id
        ).all()
        
        return {
            "department": {"id": department.department_id, "name": department.department_name},
            "branches": branches,
            "total": len(branches)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.put("/branches/{branch_id}", status_code=200)
def update_branch(
    branch_id: int,
    request: BranchRequest,
    db: db_dependancy,
    current_user=Depends(require_permission("edit"))
):
    """Update branch details"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can update branches")
        
        branch = db.query(BranchModel).filter(
            BranchModel.branch_id == branch_id
        ).first()
        
        if not branch:
            raise HTTPException(status_code=404, detail=f"Branch with id {branch_id} not found")
        
        # Verify new department exists
        department = db.query(DepartmentModel).filter(
            DepartmentModel.department_id == request.department_id
        ).first()
        
        if not department:
            raise HTTPException(status_code=404, detail=f"Department with id {request.department_id} not found")
        
        branch.department_id = request.department_id
        branch.branch_name = request.branch_name
        branch.location = request.location
        
        db.commit()
        db.refresh(branch)
        
        return {
            "msg": "Branch updated successfully",
            "branch": branch
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@route.delete("/branches/{branch_id}", status_code=200)
def delete_branch(
    branch_id: int,
    db: db_dependancy,
    current_user=Depends(require_permission("delete"))
):
    """Delete branch"""
    try:
        if current_user["role"].value not in ["admin", "superAdmin"]:
            raise HTTPException(status_code=403, detail="Only admins can delete branches")
        
        branch = db.query(BranchModel).filter(
            BranchModel.branch_id == branch_id
        ).first()
        
        if not branch:
            raise HTTPException(status_code=404, detail=f"Branch with id {branch_id} not found")
        
        db.delete(branch)
        db.commit()
        
        return {"msg": f"Branch with id {branch_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
