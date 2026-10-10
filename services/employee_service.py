from fastapi import HTTPException, UploadFile

from repositories.employee_repository import EmployeeRepository
from repositories import file_repository
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate
from services.salary_service import SalaryService


class EmployeeService:

    def __init__(self):
        self.employee_repository = EmployeeRepository()
        self.salary_service = SalaryService()

    async def get_all_employees(self, page: int, page_size: int):
        return await self.employee_repository.get_all(page, page_size)

    async def get_employee_by_id(self, employee_id: int):
        employee = await self.employee_repository.get_by_id(employee_id)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with id {employee_id} not found",
            )

        return employee

    async def create_employee(self, employee: EmployeeCreate):
        salary_details = self.salary_service.calculate(
            employee.salary,
            employee.experience,
        )

        employee_record = {
            "name": employee.name,
            "salary": employee.salary,
            "experience": employee.experience,
            **salary_details,
        }

        employee_id = await self.employee_repository.create(employee_record)

        return {
            "message": "Employee created successfully",
            "id": employee_id,
            **salary_details,
        }

    async def update_employee(
        self,
        employee_id: int,
        employee: EmployeeCreate,
    ):
        salary_details = self.salary_service.calculate(
            employee.salary,
            employee.experience,
        )

        employee_record = {
            "name": employee.name,
            "salary": employee.salary,
            "experience": employee.experience,
            **salary_details,
        }

        await self.employee_repository.update(
            employee_id,
            employee_record,
        )

        return {
            "message": "Employee updated successfully",
            "id": employee_id,
            **salary_details,
        }

    async def delete_employee(self, employee_id: int):
        await self.employee_repository.delete(employee_id)

        return {
            "message": "Employee deleted successfully",
            "id": employee_id,
        }

    async def patch_employee(
        self,
        employee_id: int,
        employee: EmployeeUpdate,
    ):
        existing_employee = await self.employee_repository.get_by_id(employee_id)

        if existing_employee is None:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with id {employee_id} not found",
            )

        updates = employee.model_dump(exclude_unset=True)

        name = updates.get("name", existing_employee["name"])
        salary = updates.get("salary", existing_employee["salary"])
        experience = updates.get("experience", existing_employee["experience"])

        salary_details = self.salary_service.calculate(salary, experience)

        employee_record = {
            "name": name,
            "salary": salary,
            "experience": experience,
            **salary_details,
        }

        await self.employee_repository.patch(
            employee_id,
            employee_record,
            employee.model_fields_set,
        )

        return {
            "id": employee_id,
            **employee_record,
        }

    async def search_employees(
        self,
        name: str | None = None,
        salary: int | None = None,
        experience: int | None = None,
    ):
        return await self.employee_repository.search_employees(
            name,
            salary,
            experience,
        )

    async def upload_employee_resume(
        self,
        employee_id: int,
        file: UploadFile,
    ):
        employee = await self.employee_repository.get_by_id(employee_id)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )

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

        file_path = await file_repository.save_file(file)

        await self.employee_repository.save_resume_path(
            employee_id,
            file_path,
        )

        return {
            "message": "Resume uploaded successfully",
            "employee_id": employee_id,
            "file_path": file_path,
        }


# Create one service instance for the router to use.
employee_service = EmployeeService()
