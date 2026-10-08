from pydantic import BaseModel, Field, field_validator


class EmployeeCreate(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, default=" ")
    salary: int = Field(gt=0, default=5000)
    experience: int = Field(ge=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name cannot be empty")
        return value


class EmployeeResponse(EmployeeCreate):
    pass


class EmployeeCreatedResponse(BaseModel):
    message: str
    id: int = Field(gt=0)
    annual_salary: int
    bonus: int | float
    tax: int | float
    net_salary: int | float


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)

    salary: int | None = Field(default=None, gt=0)

    experience: int | None = Field(default=None, ge=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Name cannot be blank")

        return value
