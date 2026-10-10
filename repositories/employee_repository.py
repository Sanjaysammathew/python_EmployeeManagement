from psycopg.errors import UniqueViolation
from database import get_connection
from fastapi import HTTPException


class EmployeeRepository:

    async def get_all(self, page: int, page_size: int):
        connection = await get_connection()

        try:
            offset = (page - 1) * page_size

            async with connection.cursor() as cursor:
                query = """
                    SELECT *
                    FROM employee
                    ORDER BY id
                    LIMIT %s OFFSET %s
                """
                await cursor.execute(query, (page_size, offset))
                employees = await cursor.fetchall()

            returned = len(employees)

            return {
                "data": employees,
                "meta": {
                    "page": page,
                    "page_size": page_size,
                    "returned": returned,
                    "has_previous": page > 1,
                    "has_next": returned == page_size,
                },
            }

        finally:
            await connection.close()

    async def get_by_id(self, employee_id: int):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "SELECT * FROM employee WHERE id = %s",
                    (employee_id,),
                )
                return await cursor.fetchone()

        finally:
            await connection.close()

    async def create(self, employee: dict) -> int:
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                query = """
                    INSERT INTO employee
                    (name, salary, experience, annual_salary,
                     bonus, tax, net_salary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """

                values = (
                    employee["name"],
                    employee["salary"],
                    employee["experience"],
                    employee["annual_salary"],
                    employee["bonus"],
                    employee["tax"],
                    employee["net_salary"],
                )

                try:
                    await cursor.execute(query, values)
                    result = await cursor.fetchone()
                    await connection.commit()
                    return result["id"]

                except UniqueViolation:
                    await connection.rollback()
                    raise HTTPException(
                        status_code=409,
                        detail="Employee already exists",
                    )

        finally:
            await connection.close()

    async def update(self, employee_id: int, employee: dict) -> None:
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                query = """
                    UPDATE employee
                    SET name = %s,
                        salary = %s,
                        experience = %s,
                        annual_salary = %s,
                        bonus = %s,
                        tax = %s,
                        net_salary = %s
                    WHERE id = %s
                """

                values = (
                    employee["name"],
                    employee["salary"],
                    employee["experience"],
                    employee["annual_salary"],
                    employee["bonus"],
                    employee["tax"],
                    employee["net_salary"],
                    employee_id,
                )

                await cursor.execute(query, values)

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Employee with id {employee_id} not found",
                    )

            await connection.commit()

        finally:
            await connection.close()

    async def delete(self, employee_id: int) -> None:
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM employee WHERE id = %s",
                    (employee_id,),
                )

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Employee with id {employee_id} not found",
                    )

            await connection.commit()

        finally:
            await connection.close()

    async def patch(
        self,
        employee_id: int,
        employee: dict,
        changed_fields: set,
    ) -> None:
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                set_parts = []
                values = []

                for field in ("name", "salary", "experience"):
                    if field in changed_fields:
                        set_parts.append(f"{field} = %s")
                        values.append(employee[field])

                # Recalculate stored salary fields when salary
                # or experience changes.
                if {"salary", "experience"} & changed_fields:
                    for field in ("annual_salary", "bonus", "tax", "net_salary"):
                        set_parts.append(f"{field} = %s")
                        values.append(employee[field])

                if not set_parts:
                    return

                query = f"""
                    UPDATE employee
                    SET {", ".join(set_parts)}
                    WHERE id = %s
                """

                values.append(employee_id)
                await cursor.execute(query, tuple(values))

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Employee with id {employee_id} not found",
                    )

            await connection.commit()

        finally:
            await connection.close()

    async def search_employees(
        self,
        name: str | None = None,
        salary: int | None = None,
        experience: int | None = None,
    ):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                query = "SELECT * FROM employee"
                conditions = []
                values = []

                if name is not None:
                    conditions.append("name ILIKE %s")
                    values.append(f"%{name}%")

                if salary is not None:
                    conditions.append("salary = %s")
                    values.append(salary)

                if experience is not None:
                    conditions.append("experience = %s")
                    values.append(experience)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                query += " ORDER BY id"

                await cursor.execute(query, tuple(values))
                return await cursor.fetchall()

        finally:
            await connection.close()

    async def save_resume_path(self, employee_id: int, file_path: str) -> None:
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE employee
                    SET resume_path = %s
                    WHERE id = %s
                    """,
                    (file_path, employee_id),
                )

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Employee with id {employee_id} not found",
                    )

            await connection.commit()

        except Exception:
            await connection.rollback()
            raise

        finally:
            await connection.close()
