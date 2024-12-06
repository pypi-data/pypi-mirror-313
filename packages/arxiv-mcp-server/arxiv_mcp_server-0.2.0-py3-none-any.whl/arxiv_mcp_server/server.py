"""
Arxiv MCP Server
===============

This module implements an MCP (Message Control Protocol) server for interacting with arXiv.
It provides capabilities for searching papers and downloading them as resources.
"""

import mcp
import asyncio
from typing import Dict, Any, List
from .config import Settings
import mcp.types as types
from mcp.server import Server, InitializationOptions, NotificationOptions
from .tools import search_tool, download_tool, handle_search, handle_download
from .resources import ResourceManager

# Initialize server settings and resource manager
settings = Settings()
server = Server(settings.APP_NAME)
resource_manager = ResourceManager()


@server.list_tools()
def list_tools() -> List[types.Tool]:
    """List available arXiv research tools."""
    return [search_tool, download_tool]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls for arXiv research functionality."""
    try:
        if name == "search_papers":
            return await handle_search(arguments)
        elif name == "download_paper":
            return await handle_download(arguments)
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@server.list_resources()
async def list_resources() -> List[types.Resource]:
    """List available paper resources."""
    return await resource_manager.list_resources()


@server.read_resource()
async def read_resource(uri: str) -> bytes:
    """Read the content of a paper resource."""
    return await resource_manager.read_resource(uri)


async def main():
    """
    Main entry point for the arXiv MCP server.
    Sets up and runs the server using stdin/stdout streams.
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=settings.APP_NAME,
                server_version=settings.APP_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
