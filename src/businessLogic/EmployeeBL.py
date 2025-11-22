from src.models.EmpModel import Employee

employees=[]

def get_employee_data(id: int = None) -> Employee:
    # Perform some logic with the user data
    if id is not None:
        for emp in employees:
            print(f"Fetching employee data for ID: {id}")

            if emp.id == id:
                return emp
    return None

def get_employee_list() -> list[Employee]:
    # Logic to get all employees
    return employees

def create_employee(employee: Employee) -> Employee:
    # Logic to create a new employee
    employees.append(employee)
    return employee