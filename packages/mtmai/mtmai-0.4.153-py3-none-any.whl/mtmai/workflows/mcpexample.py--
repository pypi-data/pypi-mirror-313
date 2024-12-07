from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mtmai.workflows.wfapp import wfapp
from mtmaisdk import Context

LOG = structlog.get_logger()

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command=".venv/bin/mtmai",
    args=[
        "mcpserver",
    ],  # Optional command line arguments
    env=None,  # Optional environment variables
)


@asynccontextmanager
async def get_mcp_session() -> AsyncGenerator[any, any]:
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                yield session

    except Exception as e:
        LOG.error("Failed to create MCP session", exc_info=e)
        raise  # Re-raise the exception after logging


@wfapp.workflow(on_events=["mcpclientexample"])
class FlowMcpClientExample:
    @wfapp.step()
    async def entry(self, ctx: Context):
        ctx.log("FlowMcpClientExample entry")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # session = await get_mcp_session()
                # ctx.log("开始连接")
                # Initialize the connection
                await session.initialize()
                ctx.log("mcp client session 初始化完成")
                # List available resources
                # resources = await session.list_resources()
                # ctx.log("列出资源", str(resources))

                # List available prompts
                prompts = await session.list_prompts()
                ctx.log("列出资源", str(prompts))

                return {
                    "status": "ok",
                }

    @wfapp.step(parents=["entry"])
    async def hello_flow_step2(self, context: Context):
        context.put_stream("hello from DemoTimerFlow load_docs")
        return {
            "status": "making sense of the docs",
        }


async def run_example_mcp_client():
    async with get_mcp_session() as session:
        # List available resources
        resources = await session.list_resources()

        # List available prompts
        prompts = await session.list_prompts()

        # List available tools
        tools = await session.list_tools()

        # Read a resource
        resource = await session.read_resource("file://some/path")

        # Call a tool
        result = await session.call_tool("tool-name", arguments={"arg1": "value"})

        # Get a prompt
        prompt = await session.get_prompt("prompt-name", arguments={"arg1": "value"})
