# Terminal calculator

## Setup, run, and test

From the repository root, use Python 3.12 or newer.

```console
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS or Linux, or `.\.venv\Scripts\Activate.ps1` in Windows PowerShell. Then run:

```console
python -m pip install -r requirements.txt
python -m calculator
python -m pytest --cov=calculator --cov-report=term-missing --cov-fail-under=100
```

## Example session

```text
calculator> add 5 3
8.0
calculator> subtract -1.5 .5
-2.0
calculator> multiply 2 4
8.0
calculator> divide 6 3
2.0
calculator> divide 6 0
Cannot divide by zero
calculator> history
add 5 3 = 8.0
subtract -1.5 0.5 = -2.0
multiply 2 4 = 8.0
divide 6 3 = 2.0
calculator> exit
```

## Method types and design patterns

- **Static method.** `Operations.add(a, b)` uses its two arguments and needs neither an instance nor a class reference.
- **Class method and Factory.** `ArithmeticCalculation.create(a, b, operation)` inherits the factory from `Calculation`. The factory uses `cls` to create an instance of the concrete class that called it.
- **Instance method.** `ArithmeticCalculation.execute()` uses `self` to read the operation and operands stored on that calculation.
- **Strategy.** For `add 5 3`, the CLI selects `Operations.add` from its dictionary and passes it to the factory. Subtraction, multiplication, and division use the same path with different functions. The calculation calls whichever function it received.
- **Command.** The CLI wraps the calculation in a `CalculateCommand`, executes it, and prints the returned answer. The command records the result after successful execution. `HistoryCommand` reads the same session history.

## Object-oriented design

- **Encapsulation.** `Calculation` keeps its operands and operation together. `HistoryCommand.execute()` returns a copy to protect stored entries from edits to the returned list.
- **Abstraction.** `Calculation` requires concrete subclasses to implement `execute()`.
- **Inheritance.** `ArithmeticCalculation` inherits operand storage and the `create()` factory from `Calculation`.
- **Polymorphism.** `CalculateCommand` can call `execute()` on any concrete `Calculation` that honors the contract.
- **Composition.** A `CalculateCommand` holds a calculation, and that calculation holds an operation function.

## SOLID principles

- **Single responsibility.** The CLI handles input and output, the calculation runs the arithmetic, and the command coordinates execution and recording.
- **Open/closed.** Adding a new operation means writing a function and registering it in the CLI dictionary. The existing execution methods already accept it as a callable.
- **Liskov substitution.** A replacement calculation must return a numeric result or raise an appropriate error so the command can preserve its success-only history behavior.
- **Interface segregation.** `Calculation` requires only `execute()` from concrete subclasses.
- **Dependency inversion.** `CalculateCommand` receives a `Calculation`, and the calculation receives a callable strategy. The CLI chooses the concrete dependencies.

## Tests and GitHub Actions

The Calculator tests workflow runs the same command shown above on Python 3.12 and requires 100% line coverage. Tests check arithmetic results, command history, CLI error recovery, and shutdown via exit or EOF.

## Coverage exclusions

`Calculation.execute()` is excluded because its abstract body is a placeholder. Tests check that the abstract class cannot be constructed and exercise the concrete implementation.
