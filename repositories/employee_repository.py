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
