from pydantic import BaseModel, EmailStr, Field


class PersonalDetails(BaseModel):
    email: EmailStr
    phone_number: str = Field(min_length=7, max_length=20)
    address: str = Field(min_length=1, max_length=1000)


class EmployeePersonalCreate(BaseModel):
    personal_details: PersonalDetails


class EmployeePersonalResponse(BaseModel):
    employee_id: int
    personal_details: PersonalDetails


class EmployeeSalaryDetails(BaseModel):
    name: str
    salary: float
    experience: int
    annual_salary: float | None
    bonus: float | None
    tax: float | None
    net_salary: float | None


class EmployeeReportResponse(BaseModel):
    employee_id: int
    employee: EmployeeSalaryDetails
    personal_details: PersonalDetails
