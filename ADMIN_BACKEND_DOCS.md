# Admin Backend Documentation

This document outlines all the admin endpoints available in the transport complaint management system.

## Base URL
All admin endpoints are prefixed with `/api/admin`

## Authentication
All endpoints require admin role (admin or superAdmin). Regular users will receive a 403 Forbidden error.

---

## Dashboard & Statistics

### GET `/api/admin/dashboard`
Get admin dashboard with statistics
- **Required Role**: admin, superAdmin
- **Response**: Returns total complaints, pending, in-progress, resolved counts, and department/branch totals

---

## Complaints Management

### GET `/api/admin/complaints`
Get all complaints (admin view)
- **Required Role**: admin, superAdmin
- **Response**: List of all complaints with total count

### GET `/api/admin/complaints/{complain_id}`
Get specific complaint with assignment details
- **Required Role**: admin, superAdmin
- **Parameters**: 
  - `complain_id` (integer): ID of the complaint
- **Response**: Complaint details + associated assignment info

### GET `/api/admin/complaints/status/{status}`
Get all complaints filtered by status
- **Required Role**: admin, superAdmin
- **Parameters**: 
  - `status` (string): One of "Pending", "In Progress", "Resolved"
- **Response**: List of complaints with matching status

### PUT `/api/admin/complaints/{complain_id}/status`
Update complaint status
- **Required Role**: admin, superAdmin (edit permission)
- **Parameters**: 
  - `complain_id` (integer): ID of the complaint
- **Request Body**:
  ```json
  {
    "status": "In Progress",
    "notes": "Optional notes"
  }
  ```
- **Response**: Updated complaint with new status

---

## Assignment Management

### POST `/api/admin/complaints/{complain_id}/assign`
Assign complaint to a department and branch
- **Required Role**: admin, superAdmin (write permission)
- **Parameters**: 
  - `complain_id` (integer): ID of the complaint
- **Request Body**:
  ```json
  {
    "complain_id": 1,
    "department_id": 1,
    "branch_id": 1
  }
  ```
- **Response**: Assignment created/updated successfully
- **Note**: On assignment, complaint status automatically changes to "In Progress"

### GET `/api/admin/assignments/{complain_id}`
Get assignment details for a specific complaint
- **Required Role**: admin, superAdmin
- **Parameters**: 
  - `complain_id` (integer): ID of the complaint
- **Response**: Assignment details with department and branch info

### DELETE `/api/admin/assignments/{complaint_id}`
Remove assignment from a complaint
- **Required Role**: admin, superAdmin (delete permission)
- **Parameters**: 
  - `complaint_id` (integer): ID of the complaint
- **Response**: Confirmation message

---

## Department Management

### POST `/api/admin/departments`
Create a new department
- **Required Role**: admin, superAdmin (write permission)
- **Request Body**:
  ```json
  {
    "department_name": "Traffic Police",
    "department_code": "TP001"
  }
  ```
- **Response**: New department created

### GET `/api/admin/departments`
Get all departments
- **Required Role**: admin, superAdmin
- **Response**: List of all departments with total count

### GET `/api/admin/departments/{department_id}`
Get specific department
- **Required Role**: admin, superAdmin
- **Parameters**: 
  - `department_id` (integer): ID of the department
- **Response**: Department details

### PUT `/api/admin/departments/{department_id}`
Update department details
- **Required Role**: admin, superAdmin (edit permission)
- **Parameters**: 
  - `department_id` (integer): ID of the department
- **Request Body**:
  ```json
  {
    "department_name": "Traffic Police Updated",
    "department_code": "TP001"
  }
  ```
- **Response**: Updated department details

### DELETE `/api/admin/departments/{department_id}`
Delete department (and associated branches)
- **Required Role**: admin, superAdmin (delete permission)
- **Parameters**: 
  - `department_id` (integer): ID of the department
- **Response**: Confirmation message

---

## Branch Management

### POST `/api/admin/branches`
Create a new branch under a department
- **Required Role**: admin, superAdmin (write permission)
- **Request Body**:
  ```json
  {
    "department_id": 1,
    "branch_name": "Downtown Branch",
    "location": "123 Main Street"
  }
  ```
- **Response**: New branch created

### GET `/api/admin/branches`
Get all branches
- **Required Role**: admin, superAdmin
- **Response**: List of all branches with total count

### GET `/api/admin/branches/department/{department_id}`
Get all branches for a specific department
- **Required Role**: admin, superAdmin
- **Parameters**: 
  - `department_id` (integer): ID of the department
- **Response**: Department info + branches list

### PUT `/api/admin/branches/{branch_id}`
Update branch details
- **Required Role**: admin, superAdmin (edit permission)
- **Parameters**: 
  - `branch_id` (integer): ID of the branch
- **Request Body**:
  ```json
  {
    "department_id": 1,
    "branch_name": "Downtown Branch Updated",
    "location": "456 Main Street"
  }
  ```
- **Response**: Updated branch details

### DELETE `/api/admin/branches/{branch_id}`
Delete branch
- **Required Role**: admin, superAdmin (delete permission)
- **Parameters**: 
  - `branch_id` (integer): ID of the branch
- **Response**: Confirmation message

---

## Error Responses

All endpoints return appropriate HTTP status codes:
- **200**: Success (GET, PUT)
- **201**: Created (POST)
- **400**: Bad Request (Invalid status or data)
- **403**: Forbidden (Insufficient permissions)
- **404**: Not Found (Resource not found)
- **409**: Conflict (Duplicate resource)
- **500**: Internal Server Error

---

## Permission Levels

- **view**: Can view complaints, assignments, departments, branches
- **edit**: Can update complaints status and details
- **write**: Can assign complaints and create departments/branches
- **delete**: Can delete assignments, departments, and branches

---

## Key Models

### DepartmentModel
- `department_id` (PK)
- `department_name`
- `department_code`
- `created_at`
- `updated_at`

### BranchModel
- `branch_id` (PK)
- `department_id` (FK)
- `branch_name`
- `location`
- `created_at`
- `updated_at`

### AssignmentModel
- `assignment_id` (PK)
- `complain_id` (FK)
- `department_id` (FK)
- `branch_id` (FK)
- `assigned_at`
- `updated_at`
