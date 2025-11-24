import json
from src.schemas.EmpSchema import Employee

employees=[]

class EmployeeBL:
    def __init__(self):
        pass
            
    def get_employee_data(self, id: int = None) -> Employee:
        # Perform some logic with the user data
        if id is not None:
            for emp in employees:
                print(f"Fetching employee data for ID: {id}")

            if emp.id == id:
                return emp
        return None

    def get_employee_list(self) -> list[Employee]:
        # Logic to get all employees
        return employees

    def create_employee(self, employee: Employee) -> Employee:
        # Logic to create a new employee
        employees.append(employee)
        return employee
    
    def signup_user(self, user_data):
        # Logic to sign up a new user
        employees=[]
        user=None
        try:
            with open("users.json", "r") as file:
                usersMocks = json.load(file)
            
            for user in usersMocks:
                employees.append(Employee(**user))
            
            for emp in employees:
                if emp.email == user_data.email:
                    user = emp
                    break       
        except json.JSONDecodeError:
            print("Error: Could not decode JSON from 'example.json'. Check file format.")
        return user