# weather_server.py
from typing import List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")


@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    print("This is log from sse server")
    return "It's always freezing in Cracow"


if __name__ == "__main__":
    mcp.run(transport="sse")
