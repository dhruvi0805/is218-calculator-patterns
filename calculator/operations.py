class Operations:
    @staticmethod
    def add(a: float, b: float) -> float:
        # This method uses only a and b. No object state is needed.
        return a + b

    @staticmethod
    def subtract(a: float, b:float):
        return a - b

    @staticmethod
    def multiply(a:float, b:float):
        return a * b

    @staticmethod
    def divide(a:float, b:float):
        try:
            return a / b
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")

