"""Инструменты калькулятора2."""


def register(mcp) -> None:
    @mcp.tool
    def multiply(a: float, b: float) -> float:
        """Умножает два числа."""
        return a * b