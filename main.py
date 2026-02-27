import asyncio
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
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
    args=["/home/eslam/ai_projects/mcp-servers/mcp-crash-course/servers/math_server.py"],
)

async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session Initialized")
            tools = await load_mcp_tools(session)

            agent = create_agent(llm,tools)
            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 62 + 2 * 3?")]})
            print(result["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())
