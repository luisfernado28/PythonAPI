from dotenv import load_dotenv
from fastapi import Depends, FastAPI,status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.repositories.database import get_db
from src.services.EmployeeBL import EmployeeBL
from src.schemas.EmpSchema import Employee, EmployeeResponse, TokenSchema, UserAuth, UserOut
from src.utils.auth import create_access_token, create_refresh_token, get_hashed_password, verify_password
from src.repositories.database import Base, engine
app = FastAPI()
load_dotenv() 
Base.metadata.create_all(bind=engine)

@app.get("/employee/{employee_email}", tags=["Employees"])
def get_employee_by_email(employee_email: str, service: EmployeeBL = Depends(EmployeeBL), db: Session = Depends(get_db)):
    """Get a specific employee by email."""
    employee_data = service.get_employee_by_email(employee_email, db)
    if employee_data:
        return EmployeeResponse(
            name=employee_data.name,
            last_name=employee_data.last_name,
            email=employee_data.email,
            user_type=employee_data.user_type
        )
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

@app.get("/employees", tags=["Employees"],response_model=List[EmployeeResponse])
def get_employees(service: EmployeeBL = Depends(EmployeeBL), db: Session = Depends(get_db)):
    """Get a list of all employees."""
    employee_list = service.get_employee_list(db)
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


@app.post('/login', tags=["Login"],summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), serviceEmployee: EmployeeBL = Depends(EmployeeBL), db: Session = Depends(get_db)):
    user = serviceEmployee.get_employee_by_email(form_data.username, db)
    if  user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }