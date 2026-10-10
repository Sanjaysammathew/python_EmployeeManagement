from fastapi import APIRouter, Query, UploadFile, File

from schemas.employee_schema import EmployeeCreate, EmployeeUpdate
from services.employee_service import employee_service

router = APIRouter(prefix="/employees", tags=["Employee Details"])


@router.get("/")
async def get_employees(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    return await employee_service.get_all_employees(page, page_size)


@router.get("/search")
async def search_employees(
    name: str | None = None,
    salary: int | None = None,
    experience: int | None = None,
):
    return await employee_service.search_employees(name, salary, experience)


@router.get("/{employee_id}")
async def get_employee_by_id(employee_id: int):
    return await employee_service.get_employee_by_id(employee_id)


@router.post("/")
async def create_employee(employee: EmployeeCreate):
    return await employee_service.create_employee(employee)


@router.put("/{employee_id}")
async def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
):
    return await employee_service.update_employee(employee_id, employee)


@router.patch("/{employee_id}")
async def patch_employee(
    employee_id: int,
    employee: EmployeeUpdate,
):
    return await employee_service.patch_employee(employee_id, employee)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    return await employee_service.delete_employee(employee_id)


@router.post("/{employee_id}/resume")
async def upload_resume(
    employee_id: int,
    file: UploadFile = File(...),
):
    return await employee_service.upload_employee_resume(employee_id, file)
