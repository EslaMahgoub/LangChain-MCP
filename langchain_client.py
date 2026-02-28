import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv()

LLM_CONFIG = {
    "base_url": "https://openrouter.ai/api/v1",
    "api_key": os.getenv("OPENROUTER_API_KEY"),
    "model": "gpt-5-nano",
    "temperature": 0,
}

llm = ChatOpenAI(**LLM_CONFIG)


async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": [
                    "/home/eslam/ai_projects/mcp-servers/mcp-crash-course/servers/math_server.py"
                ],
            },
            "weather": {
                "transport": "sse",
                "url": "http://localhost:8000/sse",
            },
        }
    )

    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    result = await agent.ainvoke(
        # {"messages": [HumanMessage(content="What is 5 + 123?")]}
        {"messages": [HumanMessage(content="What is the weather in Cracow?")]}
    )
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
