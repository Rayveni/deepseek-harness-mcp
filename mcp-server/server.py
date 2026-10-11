# server.py
#
# Точка входа MCP-сервера: создаёт приложение FastMCP и запускает транспорт.
# Вся логика инструментов (tools) и промптов живёт в отдельных модулях
# (пакет tools/) и подключается через register_tools().
from fastmcp import FastMCP
from tools import register_tools

# stateless_http УБРАН из конструктора
mcp = FastMCP(name="CalculatorServer")

# Регистрация инструментов и промптов из отдельных модулей
register_tools(mcp)

if __name__ == "__main__":
    # stateless_http передается в run()
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        stateless_http=True,
    )
