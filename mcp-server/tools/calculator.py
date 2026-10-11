"""Инструменты калькулятора."""


def register(mcp) -> None:
    @mcp.tool
    def add(a: float, b: float) -> float:
        """Складывает два числа."""
        return a + b
