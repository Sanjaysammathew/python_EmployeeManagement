from repositories import employee_repository
from schemas.employee_schema import EmployeeCreate


def get_all_employees():
    return employee_repository.get_all()


def get_employee_by_id(employee_id: int):
    return employee_repository.get_by_id(employee_id)


def create_employee(employee: EmployeeCreate) -> dict[str, int | float | str]:

    annual_salary = employee.salary * 12

    bonus = 0
    tax = 0

    if employee.experience >= 3:
        bonus = employee.salary * 0.10
        tax = employee.salary * 0.05

    net_salary = annual_salary + bonus - tax

    employee_record = {
        "id": employee.id,
        "name": employee.name,
        "salary": employee.salary,
        "experience": employee.experience,
        "annual_salary": annual_salary,
        "bonus": bonus,
        "tax": tax,
        "net_salary": net_salary,
    }

    employee_repository.create(employee_record)

    return {
        "message": "Employee created successfully",
        "id": employee.id,
        "annual_salary": annual_salary,
        "bonus": bonus,
        "tax": tax,
        "net_salary": net_salary,
    }


def update_employee(employee_id: int, employee: EmployeeCreate):

    annual_salary = employee.salary * 12

    bonus = 0
    tax = 0

    if employee.experience >= 3:
        bonus = employee.salary * 0.10
        tax = employee.salary * 0.05

    net_salary = annual_salary + bonus - tax

    employee_record = {
        "name": employee.name,
        "salary": employee.salary,
        "experience": employee.experience,
        "annual_salary": annual_salary,
        "bonus": bonus,
        "tax": tax,
        "net_salary": net_salary,
    }

    employee_repository.update(employee_id, employee_record)

    return {
        "message": "Employee updated successfully",
        "id": employee_id,
        "annual_salary": annual_salary,
        "bonus": bonus,
        "tax": tax,
        "net_salary": net_salary,
    }


def delete_employee(employee_id: int):

    employee_repository.delete(employee_id)

    return {"message": "Employee deleted successfully", "id": employee_id}
