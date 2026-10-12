"""Пакет модулей инструментов MCP-сервера.

Каждый инструмент (или группа связанных инструментов) определяется в своём
модуле и экспортирует функцию register(mcp), которая декорирует функции
декораторами @mcp.tool / @mcp.prompt. Новые модули добавляются в список
import'ов ниже — server.py про них ничего не знает.
"""

from . import calculator
from . import code_reviewer


def register_tools(mcp) -> None:
    """Зарегистрировать все инструменты и промпты в приложении FastMCP."""
    calculator.register(mcp)
    code_reviewer.register(mcp)
