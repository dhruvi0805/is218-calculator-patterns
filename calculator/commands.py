"""Commands for calculating and reading session history."""

from .calculation import Calculation


class CalculateCommand:
    def __init__(self, calculation: Calculation, history: list[str], name: str):
        self.calculation = calculation
        self.history = history
        self.name = name

    def execute(self) -> float:
        result = self.calculation.execute()
        self.history.append(
            f"{self.name} {self.calculation.a:g} {self.calculation.b:g} = {result}"
        )
        return result


class HistoryCommand:
    def __init__(self, history: list[str]):
        self.history = history

    def execute(self) -> list[str]:
        return self.history.copy()
