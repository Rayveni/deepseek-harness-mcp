from . import plantuml,mcp_assets


def register_tools(mcp) -> None:
    """Зарегистрировать все инструменты и промпты в приложении FastMCP."""
    plantuml.register(mcp)
    mcp_assets.register(mcp)
