class SalaryService:

    def calculate_annual_salary(self, salary: int) -> int:
        return salary * 12

    def calculate_bonus(self, salary: int, experience: int) -> float:
        if experience >= 3:
            return salary * 0.10

        return 0

    def calculate_tax(self, salary: int, experience: int) -> float:
        if experience >= 3:
            return salary * 0.05

        return 0

    def calculate(self, salary: int, experience: int) -> dict:

        annual_salary = self.calculate_annual_salary(salary)

        bonus = self.calculate_bonus(salary, experience)

        tax = self.calculate_tax(salary, experience)

        net_salary = annual_salary + bonus - tax

        return {
            "annual_salary": annual_salary,
            "bonus": bonus,
            "tax": tax,
            "net_salary": net_salary,
        }
