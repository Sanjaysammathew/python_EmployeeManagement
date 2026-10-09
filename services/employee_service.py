from repositories import employee_repository, file_repository
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate
from services.salary_service import SalaryService
from fastapi import HTTPException, UploadFile

salary_service = SalaryService()


async def get_all_employees(page: int, page_size: int):
    return await employee_repository.get_all(page, page_size)


async def get_employee_by_id(employee_id: int):
    return await employee_repository.get_by_id(employee_id)


async def create_employee(employee: EmployeeCreate):

    salary_details = salary_service.calculate(employee.salary, employee.experience)

    employee_record = {
        "name": employee.name,
        "salary": employee.salary,
        "experience": employee.experience,
        "annual_salary": salary_details["annual_salary"],
        "bonus": salary_details["bonus"],
        "tax": salary_details["tax"],
        "net_salary": salary_details["net_salary"],
    }

    # Database generates the ID and returns it
    employee_id = await employee_repository.create(employee_record)

    return {
        "message": "Employee created successfully",
        "id": employee_id,
        **salary_details,
    }


async def update_employee(employee_id: int, employee: EmployeeCreate):

    # Normal Python calculation → NO await
    salary_details = salary_service.calculate(employee.salary, employee.experience)

    employee_record = {
        "name": employee.name,
        "salary": employee.salary,
        "experience": employee.experience,
        **salary_details,
    }

    # Database operation → await
    await employee_repository.update(employee_id, employee_record)

    return {
        "message": "Employee updated successfully",
        "id": employee_id,
        **salary_details,
    }


async def delete_employee(employee_id: int):

    # Database operation → await
    await employee_repository.delete(employee_id)

    return {
        "message": "Employee deleted successfully",
        "id": employee_id,
    }


async def patch_employee(employee_id: int, employee: EmployeeUpdate):

    existing_employee = await employee_repository.get_by_id(employee_id)

    if existing_employee is None:
        raise HTTPException(
            status_code=404, detail=f"Employee with id {employee_id} not found"
        )

    updates = employee.model_dump(exclude_unset=True)

    name = updates.get("name", existing_employee["name"])

    salary = updates.get("salary", existing_employee["salary"])

    experience = updates.get("experience", existing_employee["experience"])

    salary_details = salary_service.calculate(salary, experience)

    employee_record = {
        "name": name,
        "salary": salary,
        "experience": experience,
        **salary_details,
    }

    await employee_repository.patch(
        employee_id, employee_record, employee.model_fields_set
    )

    return employee_record


async def search_employees(
    name: str | None = None,
    salary: int | None = None,
    experience: int | None = None,
):
    return await employee_repository.search_employees(name, salary, experience)


async def upload_employee_resume(
    employee_id: int,
    file: UploadFile,
):
    # 1. Check whether the employee exists
    employee = await employee_repository.get_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    # 2. Allow PDF files only
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file content type",
        )

    # 3. Save the actual file
    file_path = await file_repository.save_file(file)

    # 4. Store the path in PostgreSQL
    await employee_repository.save_resume_path(
        employee_id,
        file_path,
    )

    return {
        "message": "Resume uploaded successfully",
        "employee_id": employee_id,
        "file_path": file_path,
    }
