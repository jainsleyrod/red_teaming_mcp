from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
import logfire

load_dotenv()
logfire.configure()  
logfire.instrument_pydantic_ai()

model = OpenAIChatModel("gpt-4o-mini", provider="github")

calc_server = MCPServerStreamableHTTP('http://localhost:8000/mcp')  

agent = Agent(
    model = model, 
    toolsets=[calc_server,]
    )  

async def main():
    async with agent:  
        result = await agent.run('What is 7 multiply 5?')
    print(result.output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())