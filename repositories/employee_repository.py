from psycopg.errors import UniqueViolation
from database import get_connection
from fastapi import HTTPException


async def get_all():
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM employee")
            return await cursor.fetchall()

    finally:
        await connection.close()


async def get_by_id(employee_id: int):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:

            query = """
                SELECT *
                FROM employee
                WHERE id = %s
            """

            await cursor.execute(query, (employee_id,))

            employee = await cursor.fetchone()

            if employee is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Employee with id {employee_id} not found",
                )

            return employee

    finally:
        await connection.close()


async def create(employee: dict) -> None:
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:

            query = """
                INSERT INTO employee
                (id, name, salary, experience, annual_salary,
                 bonus, tax, net_salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                employee["id"],
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

            except UniqueViolation:
                raise HTTPException(
                    status_code=409,
                    detail=f"Employee with id {employee['id']} already exists",
                )

        await connection.commit()

    finally:
        await connection.close()


async def update(employee_id: int, employee: dict) -> None:
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


async def delete(employee_id: int) -> None:
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:

            query = """
                DELETE FROM employee
                WHERE id = %s
            """

            await cursor.execute(query, (employee_id,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"Employee with id {employee_id} not found",
                )

        await connection.commit()

    finally:
        await connection.close()


async def patch(employee_id: int, employee: dict, changed_fields: set):
    connection = await get_connection()

    try:
        async with connection.cursor() as cursor:

            set_parts = []
            values = []

            if "name" in changed_fields:
                set_parts.append("name = %s")
                values.append(employee["name"])

            if "salary" in changed_fields:
                set_parts.append("salary = %s")
                values.append(employee["salary"])

            if "experience" in changed_fields:
                set_parts.append("experience = %s")
                values.append(employee["experience"])

            if not set_parts:
                return

            query = f"""
                UPDATE employee
                SET {", ".join(set_parts)}
                WHERE id = %s
            """

            values.append(employee_id)

            await cursor.execute(query, values)

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail=f"Employee with id {employee_id} not found"
                )

        await connection.commit()

    finally:
        await connection.close()
