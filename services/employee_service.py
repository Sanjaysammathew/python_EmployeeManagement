from repositories import employee_repository
from schemas.employee_schema import EmployeeCreate
from services.salary_service import SalaryService

salary_service = SalaryService()


def get_all_employees():
    return employee_repository.get_all()


def get_employee_by_id(employee_id: int):
    return employee_repository.get_by_id(employee_id)


def create_employee(employee: EmployeeCreate):

    salary_details = salary_service.calculate(employee.salary, employee.experience)

    employee_record = {
        "id": employee.id,
        "name": employee.name,
        "salary": employee.salary,
        "experience": employee.experience,
        "annual_salary": salary_details["annual_salary"],
        "bonus": salary_details["bonus"],
        "tax": salary_details["tax"],
        "net_salary": salary_details["net_salary"],
    }

    employee_repository.create(employee_record)

    return {
        "message": "Employee created successfully",
        "id": employee.id,
        **salary_details,
    }


def update_employee(employee_id: int, employee: EmployeeCreate):

    salary_details = salary_service.calculate(employee.salary, employee.experience)

    employee_record = {
        "name": employee.name,
        "salary": employee.salary,
        "experience": employee.experience,
        **salary_details,
    }

    employee_repository.update(employee_id, employee_record)

    return {
        "message": "Employee updated successfully",
        "id": employee_id,
        **salary_details,
    }


def delete_employee(employee_id: int):

    employee_repository.delete(employee_id)

    return {"message": "Employee deleted successfully", "id": employee_id}
