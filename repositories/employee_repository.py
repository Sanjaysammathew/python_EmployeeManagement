from psycopg.errors import UniqueViolation

from database import get_connection
from fastapi import HTTPException


def get_all():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employee")
            return cursor.fetchall()

    finally:
        connection.close()


def get_by_id(employee_id: int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT *
                FROM employee
                WHERE id = %s
            """

            cursor.execute(query, (employee_id,))

            employee = cursor.fetchone()

            if employee is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Employee with id {employee_id} not found",
                )

            return employee

    finally:
        connection.close()


def create(employee: dict) -> None:
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

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
                cursor.execute(query, values)

            except UniqueViolation:
                raise HTTPException(
                    status_code=409,
                    detail=f"Employee with id {employee['id']} already exists",
                )

        connection.commit()

    finally:
        connection.close()


def update(employee_id: int, employee: dict) -> None:

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

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

            cursor.execute(query, values)

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"Employee with id {employee_id} not found",
                )

        connection.commit()

    finally:
        connection.close()


def delete(employee_id: int) -> None:

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                DELETE FROM employee
                WHERE id = %s
            """

            cursor.execute(query, (employee_id,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"Employee with id {employee_id} not found",
                )

        connection.commit()

    finally:
        connection.close()
