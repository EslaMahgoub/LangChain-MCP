import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

LLM_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "model": "gpt-5-nano",
    "temperature": 0,
}

llm = ChatOpenAI(**LLM_CONFIG)

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/home/eslam/ai_projects/mcp-servers/mcp-crash-course/servers/weather_server.py"],
)

async def main():
    print("Hello from mcp-crash-course!")

if __name__ == "__main__":
    asyncio.run(main())
