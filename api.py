from fastapi import Depends, FastAPI
from typing import List

# import BL functions with different local names to avoid shadowing
from src.models.EmpModel import Employee, EmployeeResponse
from src.businessLogic.EmployeeBL import get_employee_data as bl_get_employee_data, create_employee as bl_create_employee, get_employee_list

app = FastAPI()
# @app.get("/employee",tags=["Employees"])
# def get_books(limit: int | None = None):
#     """Get all books, optionally limited by count."""
#     if limit:
#         return {"books": books[:limit]}
#     return {"books": books}

@app.get("/employee/{employee_id}", tags=["Employees"])
def get_employee(employee_id: int, employee_data: Employee = Depends(bl_get_employee_data)):
    """Get a specific employee by ID."""
    if employee_data:
        return EmployeeResponse(
            name=employee_data.name,
            last_name=employee_data.last_name,
            email=employee_data.email,
            user_type=employee_data.user_type
        )
    return {"error": "Employee not found"}

@app.get("/employees", tags=["Employees"],response_model=List[EmployeeResponse])
def get_employees(employee_list: List[Employee] = Depends(get_employee_list)):
    """Get a list of all employees."""
    response = []
    for emp in employee_list:
        response.append(EmployeeResponse(
            name=emp.name,
            last_name=emp.last_name,
            email=emp.email,
            user_type=emp.user_type
        ))
    return response

@app.post("/employee", tags=["Employees"], response_model=EmployeeResponse)
def create_employee_endpoint(employee: Employee, created: Employee = Depends(bl_create_employee)):
    """Create a new employee entry."""
    return EmployeeResponse(
        name=created.name,
        last_name=created.last_name,
        email=created.email,
        user_type=created.user_type
    )