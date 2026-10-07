from database import get_connection
from models import EmployeeCreate


def get_students():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM employee")

        employees = cursor.fetchall()

        cursor.close()

        return employees

    finally:
        connection.close()


def post_students(employee: EmployeeCreate):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        annual_salary = employee.salary * 12

        bonus = 0
        tax = 0

        if employee.experience >= 3:
            bonus = employee.salary * 0.10
            tax = employee.salary * 0.05

        net_salary = annual_salary + bonus - tax

        query = """
            INSERT INTO employee
            (id, name, salary, experience, annual_salary, bonus, tax, net_salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            employee.id,
            employee.name,
            employee.salary,
            employee.experience,
            annual_salary,
            bonus,
            tax,
            net_salary
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()

        return {
            "message": "Employee created successfully",
            "id": employee.id,
            "annual_salary": annual_salary,
            "bonus": bonus,
            "tax": tax,
            "net_salary": net_salary
        }

    finally:
        connection.close()