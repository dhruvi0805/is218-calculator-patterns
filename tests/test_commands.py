import pytest

from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def test_commands_record_only_successes_in_order():
    history = []
    read_history = HistoryCommand(history)
    assert read_history.execute() == []

    add = ArithmeticCalculation.create(5, 3, Operations.add)
    divide_by_zero = ArithmeticCalculation.create(5, 0, Operations.divide)
    multiply = ArithmeticCalculation.create(2, 3, Operations.multiply)

    assert CalculateCommand(add, history, "add").execute() == 8
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        CalculateCommand(divide_by_zero, history, "divide").execute()
    assert CalculateCommand(multiply, history, "multiply").execute() == 6
    expected = ["add 5 3 = 8", "multiply 2 3 = 6"]
    assert read_history.execute() == expected

    read_history.execute().clear()
    assert read_history.execute() == expected
