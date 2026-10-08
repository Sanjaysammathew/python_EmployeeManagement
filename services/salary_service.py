from decimal import Decimal


class SalaryService:

    def calculate_bonus(self, salary, experience):
        return salary * Decimal("0.10")

    def calculate_tax(self, salary):
        return salary * Decimal("0.05")

    def calculate(self, salary, experience):

        annual_salary = salary * 12

        bonus = self.calculate_bonus(salary, experience)

        tax = self.calculate_tax(salary)

        net_salary = annual_salary + bonus - tax

        return {
            "annual_salary": annual_salary,
            "bonus": bonus,
            "tax": tax,
            "net_salary": net_salary,
        }
