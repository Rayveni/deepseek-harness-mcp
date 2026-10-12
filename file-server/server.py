from fastmcp import FastMCP
from tools import register_tools

mcp = FastMCP(name="FileServer")

# Регистрация инструментов из отдельных модулей
register_tools(mcp)

if __name__ == "__main__":
    # stateless_http передается в run()
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8001,
        stateless_http=True,
    )
