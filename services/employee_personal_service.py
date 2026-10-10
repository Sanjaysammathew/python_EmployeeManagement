from fastapi import HTTPException

from repositories.employee_personal_repository import (
    EmployeePersonalRepository,
)
from repositories.employee_repository import EmployeeRepository
from schemas.employee_personal_schema import (
    EmployeePersonalCreate,
    EmployeePersonalResponse,
    PersonalDetails,
    EmployeeSalaryDetails,
    EmployeeReportResponse,
)


class EmployeePersonalService:

    def __init__(self):
        self.repository = EmployeePersonalRepository()
        self.employee_repository = EmployeeRepository()

    async def create_personal_details(
        self,
        employee_id: int,
        data: EmployeePersonalCreate,
    ):
        # Check that the employee exists first.
        employee = await self.employee_repository.get_by_id(employee_id)

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )

        details = data.personal_details.model_dump(mode="json")

        await self.repository.create(employee_id, details)

        return EmployeePersonalResponse(
            employee_id=employee_id,
            personal_details=data.personal_details,
        )

    async def get_personal_details(self, employee_id: int):
        details = await self.repository.get_by_employee_id(employee_id)

        if details is None:
            raise HTTPException(
                status_code=404,
                detail="Personal details not found",
            )

        return EmployeePersonalResponse(
            employee_id=details["employee_id"],
            personal_details=PersonalDetails(
                email=details["email"],
                phone_number=details["phone_number"],
                address=details["address"],
            ),
        )

    async def update_personal_details(
        self,
        employee_id: int,
        data: EmployeePersonalCreate,
    ):
        details = data.personal_details.model_dump(mode="json")

        await self.repository.update(employee_id, details)

        return EmployeePersonalResponse(
            employee_id=employee_id,
            personal_details=data.personal_details,
        )

    async def delete_personal_details(self, employee_id: int):
        details = await self.repository.get_by_employee_id(employee_id)

        if details is None:
            raise HTTPException(
                status_code=404,
                detail="Personal details not found",
            )

        await self.repository.delete(employee_id)

        return {
            "message": "Personal details deleted successfully",
            "employee_id": employee_id,
        }

    async def get_employee_report(self, employee_id: int):
        row = await self.repository.get_report(employee_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Employee or personal details not found",
            )

        return EmployeeReportResponse(
            employee_id=row["employee_id"],
            employee=EmployeeSalaryDetails(
                name=row["name"],
                salary=row["salary"],
                experience=row["experience"],
                annual_salary=row["annual_salary"],
                bonus=row["bonus"],
                tax=row["tax"],
                net_salary=row["net_salary"],
            ),
            personal_details=PersonalDetails(
                email=row["email"],
                phone_number=row["phone_number"],
                address=row["address"],
            ),
        )

employee_personal_service = EmployeePersonalService()
