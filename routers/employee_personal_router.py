from fastapi import APIRouter

from schemas.employee_personal_schema import (
    EmployeePersonalCreate,
    EmployeePersonalResponse,
    EmployeeReportResponse,
)
from services.employee_personal_service import employee_personal_service

router = APIRouter(prefix="/employee-personal", tags=["Employee Personal Details"])


@router.post(
    "/{employee_id}",
    response_model=EmployeePersonalResponse,
    status_code=201,
)
async def create_personal_details(
    employee_id: int,
    data: EmployeePersonalCreate,
):
    return await employee_personal_service.create_personal_details(employee_id, data)


@router.get(
    "/{employee_id}",
    response_model=EmployeePersonalResponse,
)
async def get_personal_details(employee_id: int):
    return await employee_personal_service.get_personal_details(employee_id)


@router.put(
    "/{employee_id}",
    response_model=EmployeePersonalResponse,
)
async def update_personal_details(
    employee_id: int,
    data: EmployeePersonalCreate,
):
    return await employee_personal_service.update_personal_details(employee_id, data)


@router.get(
    "/{employee_id}/report",
    response_model=EmployeeReportResponse,
)
async def get_employee_report(employee_id: int):
    return await employee_personal_service.get_employee_report(employee_id)


@router.delete("/{employee_id}")
async def delete_personal_details(employee_id: int):
    return await employee_personal_service.delete_personal_details(employee_id)
