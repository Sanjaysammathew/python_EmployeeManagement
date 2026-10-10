from database import get_connection
from fastapi import HTTPException
from psycopg.errors import UniqueViolation


class EmployeePersonalRepository:

    async def create(self, employee_id: int, details: dict):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO employee_personal_details
                        (employee_id, email, phone_number, address)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        employee_id,
                        details["email"],
                        details["phone_number"],
                        details["address"],
                    ),
                )

            await connection.commit()

        except UniqueViolation as exc:
            await connection.rollback()
            raise HTTPException(
                status_code=409,
                detail="Personal details already exist or email is already used",
            ) from exc

        finally:
            await connection.close()

    async def get_by_employee_id(self, employee_id: int):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT employee_id, email, phone_number, address
                    FROM employee_personal_details
                    WHERE employee_id = %s
                    """,
                    (employee_id,),
                )
                return await cursor.fetchone()

        finally:
            await connection.close()

    async def update(self, employee_id: int, details: dict):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    UPDATE employee_personal_details
                    SET email = %s,
                        phone_number = %s,
                        address = %s
                    WHERE employee_id = %s
                    """,
                    (
                        details["email"],
                        details["phone_number"],
                        details["address"],
                        employee_id,
                    ),
                )

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail="Personal details not found",
                    )

            await connection.commit()

        except UniqueViolation as exc:
            await connection.rollback()
            raise HTTPException(
                status_code=409,
                detail="Email address is already used",
            ) from exc

        finally:
            await connection.close()

    async def get_report(self, employee_id: int):
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT
                        e.id AS employee_id,
                        e.name,
                        e.salary,
                        e.experience,
                        e.annual_salary,
                        e.bonus,
                        e.tax,
                        e.net_salary,
                        p.email,
                        p.phone_number,
                        p.address
                    FROM employee AS e
                    INNER JOIN employee_personal_details AS p
                        ON e.id = p.employee_id
                    WHERE e.id = %s
                    """,
                    (employee_id,),
                )

                return await cursor.fetchone()

        finally:
            await connection.close()

    async def delete(self, employee_id: int) -> None:
        connection = await get_connection()

        try:
            async with connection.cursor() as cursor:
                query = """
                    DELETE FROM employee_personal_details
                    WHERE employee_id = %s
                """

                await cursor.execute(query, (employee_id,))

                if cursor.rowcount == 0:
                    raise HTTPException(
                        status_code=404,
                        detail="Personal details not found",
                    )

            await connection.commit()

        except Exception:
            await connection.rollback()
            raise

        finally:
            await connection.close()
