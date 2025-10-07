import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
import logfire

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIChatModel

load_dotenv()
logfire.configure()
logfire.instrument_pydantic_ai()

model = OpenAIChatModel("gpt-4o-mini", provider="github")

async def main():
    # Create and use MCP server with async context manager
    async with MCPServerStdio(
        command=sys.executable,
        args=["-u", "stdio_server.py"]
    ) as calc_server:
        # Create agent with the MCP server
        agent = Agent(
            model=model,
            toolsets=[calc_server],
        )
        
        # Run the agent
        result = await agent.run("What is 7 multiply 5?")
        print(result.output)

if __name__ == "__main__":
    asyncio.run(main())