import json
from src.models.empModels import UserDB
from src.schemas.EmpSchema import Employee, EmployeeType
from sqlalchemy.orm import Session

from src.utils.auth import get_hashed_password

employees=[]

class EmployeeBL:
    def __init__(self):
        pass
            
    def get_employee_by_email(self, email: str , db: Session) -> Employee:
        user=db.query(UserDB).filter(UserDB.email == email).first()
        if user is not None:
            employee=Employee(
                id=user.id,
                name=user.name,
                last_name=user.last_name,
                email=user.email,
                password=user.hashed_password,
                user_type=user.user_type
            )
            return employee
        else:
            return None
        
    def get_employee_list(self, db: Session) -> list[Employee]:
        all_users=db.query(UserDB).all()
        employees=[]
        for user in all_users:
            user=Employee(
                id=user.id,
                name=user.name,
                last_name=user.last_name,
                email=user.email,
                password=user.hashed_password,
                user_type=user.user_type
            )
            employees.append(user)

        return employees

    def create_employee(self, employee: Employee, db: Session) -> Employee:
        # Logic to create a new employee
        hashed_password = get_hashed_password(employee.password)
        new_user= UserDB(
            name=employee.name,
            last_name=employee.last_name,
            email=employee.email,
            hashed_password=hashed_password,
            user_type=employee.user_type.name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return employee
    
    def login_user(self, email: str, password: str):
        # Logic to log in a user
        employees=[]
        user=None
        try:
            with open("users.json", "r") as file:
                usersMocks = json.load(file)
            
            for user in usersMocks:
                employees.append(Employee(**user))
            
            for emp in employees:
                if emp.email == email:
                    user = emp
                    break       
        except json.JSONDecodeError:
            print("Error: Could not decode JSON from 'example.json'. Check file format.")
        return user