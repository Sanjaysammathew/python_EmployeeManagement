from dataclasses import dataclass
from decimal import decimal


@dataclass
class employee_record:
    id: int
    name: str
    salary: int
    experience: int
    annual_salary: int | decimal | float
    bonus: int | decimal | float
    tax: int | float | decimal
