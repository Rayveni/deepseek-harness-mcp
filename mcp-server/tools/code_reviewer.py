"""Инструменты калькулятора2."""


def register(mcp) -> None:
    @mcp.tool
    def minus(a: float, b: float) -> float:
        """Вычитает два числа."""
        return a - b