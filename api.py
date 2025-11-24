from http.client import HTTPException
from fastapi import Depends, FastAPI,status
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.repositories.database import get_db
from src.services.EmployeeBL import EmployeeBL
from src.schemas.EmpSchema import Employee, EmployeeResponse, TokenSchema, UserAuth, UserOut
from src.utils.auth import create_access_token, create_refresh_token, get_hashed_password, verify_password
from src.repositories.database import Base, engine
app = FastAPI()

Base.metadata.create_all(bind=engine)
# @app.get("/employee",tags=["Employees"])
# def get_books(limit: int | None = None):
#     """Get all books, optionally limited by count."""
#     if limit:
#         return {"books": books[:limit]}
#     return {"books": books}

@app.get("/employee/{employee_id}", tags=["Employees"])
def get_employee(employee_id: int, bl: Employee = Depends(EmployeeBL)):
    """Get a specific employee by ID."""
    employee_data = bl.get_employee_data(employee_id)
    if employee_data:
        return EmployeeResponse(
            name=employee_data.name,
            last_name=employee_data.last_name,
            email=employee_data.email,
            user_type=employee_data.user_type
        )
    return {"error": "Employee not found"}

@app.get("/employees", tags=["Employees"],response_model=List[EmployeeResponse])
def get_employees(bl: EmployeeBL = Depends(EmployeeBL), db: Session = Depends(get_db)):
    """Get a list of all employees."""
    employee_list = bl.get_employee_list(db)
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
def create_employee_endpoint(employee: Employee, bl: EmployeeBL = Depends(EmployeeBL), db: Session = Depends(get_db)):
    """Create a new employee entry."""
    created = bl.create_employee(employee,db)
    return EmployeeResponse(
        name=created.name,
        last_name=created.last_name,
        email=created.email,
        user_type=created.user_type
    )

@app.post('/signup', tags=["Login"], summary="Log in user", response_model=UserOut)
async def signup(data: UserAuth, serviceEmployee: EmployeeBL = Depends(EmployeeBL)):
    # querying database to check if user already exist
    user = serviceEmployee.signup_user(data)
    if user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': user.email,
        'password': get_hashed_password(user.password),
        'id': 12
    }
    return user

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), serviceEmployee: EmployeeBL = Depends(EmployeeBL)):
    user = serviceEmployee.login_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    hashed_pass = form_data.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }