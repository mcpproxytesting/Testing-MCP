import asyncio
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TARGET_SERVER_PATH = "server.py"

anthropic = Anthropic()


async def run_host(user_prompt: str):
    server_params = StdioServerParameters(command="python", args=[TARGET_SERVER_PATH])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to MCP server.")

            tools_result = await session.list_tools()
            print(f"Discovered {len(tools_result.tools)} tool(s): "
                  f"{[t.name for t in tools_result.tools]}")

            claude_tools = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.input_schema,  # v2 field name
                }
                for t in tools_result.tools
            ]

            messages = [{"role": "user", "content": user_prompt}]

            while True:
                response = anthropic.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    tools=claude_tools,
                    messages=messages,
                )
                messages.append({"role": "assistant", "content": response.content})

                if response.stop_reason != "tool_use":
                    for block in response.content:
                        if block.type == "text":
                            print("\nFinal answer:", block.text)
                    return

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"\n→ Calling tool: {block.name}({block.input})")
                        result = await session.call_tool(block.name, block.input)
                        output_text = result.content[0].text
                        print(f"← Result: {output_text}")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output_text,
                        })

                messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    prompt = ("Enter your prompt: ")
    asyncio.run(run_host(prompt))