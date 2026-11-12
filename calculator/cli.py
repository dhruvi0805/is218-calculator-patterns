"""Read and execute calculator commands in the terminal."""

from .calculation import ArithmeticCalculation
from .commands import CalculateCommand, HistoryCommand
from .operations import Operations

OPERATIONS = {
    "add": Operations.add,
    "subtract": Operations.subtract,
    "multiply": Operations.multiply,
    "divide": Operations.divide,
}


def main() -> None:
    history: list[str] = []
    while True:
        try:
            parts = input("calculator> ").split()
        except EOFError:
            print()
            return

        if not parts:
            continue

        name, *operands = parts
        if name in ("exit", "history"):
            if operands:
                print(f"Usage: {name}")
                continue
            if name == "exit":
                return
            entries = HistoryCommand(history).execute()
            print("\n".join(entries) if entries else "History is empty.")
            continue

        if name not in OPERATIONS:
            print(f"Unknown command: {name}")
            continue
        if len(operands) != 2:
            print(f"Usage: {name} <number> <number>")
            continue
        try:
            a, b = map(float, operands)
        except ValueError:
            print("Invalid number. Enter two numbers.")
            continue

        # Select the operation, build the calculation, run the command, and print.
        calculation = ArithmeticCalculation.create(a, b, OPERATIONS[name])
        try:
            result = CalculateCommand(calculation, history, name).execute()
        except ValueError as error:
            print(error)
        else:
            print(result)
