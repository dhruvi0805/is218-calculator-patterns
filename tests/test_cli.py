import runpy

from calculator.cli import main


def test_cli_recovers_and_shows_successful_history(monkeypatch, capsys):
    inputs = iter([
        " ", "history", "history extra", "bogus", "add 1", "multiply 1 2 3",
        "subtract wrong 2", "divide 1 0", "add 5 3", "subtract -1.5 .5",
        "multiply -3 0", "divide 6 3", "history", "exit extra", "exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt: next(inputs))

    main()

    assert capsys.readouterr().out.splitlines() == [
        "History is empty.",
        "Usage: history",
        "Unknown command: bogus",
        "Usage: add <number> <number>",
        "Usage: multiply <number> <number>",
        "Invalid number. Enter two numbers.",
        "Cannot divide by zero",
        "8.0", "-2.0", "-0.0", "2.0",
        "add 5 3 = 8.0",
        "subtract -1.5 0.5 = -2.0",
        "multiply -3 0 = -0.0",
        "divide 6 3 = 2.0",
        "Usage: exit",
    ]


def test_module_entry_point_handles_eof(monkeypatch, capsys):
    def end_input(prompt):
        assert prompt == "calculator> "
        raise EOFError

    monkeypatch.setattr("builtins.input", end_input)

    runpy.run_module("calculator", run_name="__main__")

    assert capsys.readouterr().out == "\n"
