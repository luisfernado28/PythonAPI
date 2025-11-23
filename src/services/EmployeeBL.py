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