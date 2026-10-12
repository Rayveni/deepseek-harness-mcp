"""Инструменты калькулятора."""


def register(mcp) -> None:
    @mcp.tool
    def divide(a: float, b: float) -> float:
        """Делит два числа."""
        return a / b
