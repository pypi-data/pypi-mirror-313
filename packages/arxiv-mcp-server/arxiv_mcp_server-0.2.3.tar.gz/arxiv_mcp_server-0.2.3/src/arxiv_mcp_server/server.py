"""
Arxiv MCP Server
===============

This module implements an MCP (Message Control Protocol) server for interacting with arXiv.
It provides capabilities for searching papers and downloading them as resources.
"""

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server, InitializationOptions, AnyUrl, NotificationOptions
from typing import Dict, Any, List
from pathlib import Path

from .config import Settings
from .tools import handle_search, handle_download, handle_list_papers
from .tools import search_tool, download_tool, list_tool
from .resources import ResourceManager
import logging


# Initialize server settings and resource manager
settings = Settings()
app = Server(settings.APP_NAME)
resource_manager = ResourceManager()

logger = logging.getLogger("arxiv-mcp-server")
logger.setLevel(logging.INFO)


@app.set_logging_level()
async def set_logging_level(level: types.LoggingLevel) -> types.EmptyResult:
    logger.setLevel(level.upper())
    await app.request_context.session.send_log_message(
        level="debug", data=f"Log level set to {level}", logger="arxiv-mcp-server"
    )
    return types.EmptyResult()


# TODO: Try running resources with SSE. Seems to not work properly as is.
# @app.list_resources()
# async def list_resources() -> List[types.Resource]:
#     """List available paper resources."""
#     logger.info("Listing resources")
#     resources = await resource_manager.list_resources()
#     logger.info(f"Found {len(resources)} resources")
#     return resources


# @app.read_resource()
# async def read_resource(uri: AnyUrl) -> str:
#     """Read the content of a paper resource."""
#     assert uri.path is not None
#     # Load paper markdown
#     paper_id = Path(uri.path).stem
#     paper_path = resource_manager.storage._get_paper_path(paper_id)
#     with open(paper_path, "r") as f:
#         return f.read()


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available arXiv research tools."""
    return [
        search_tool,
        download_tool,
        list_tool,
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls for arXiv research functionality."""
    ctx = app.request_context

    if progress_token := ctx.meta.progressToken:
        # Send progress notifications via the session
        await ctx.session.send_progress_notification(
            progress_token=progress_token, progress=0.5, total=1.0
        )
    try:
        if name == "search_papers":
            return await handle_search(arguments)
        elif name == "download_paper":
            return await handle_download(arguments)
        elif name == "list_papers":
            return await handle_list_papers(arguments)
        else:
            return [types.TextContent(type="text", text=f"Error: Unknown tool {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the server async context."""
    async with mcp.server.stdio.stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name=settings.APP_NAME,
                server_version=settings.APP_VERSION,
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(resources_changed=True),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
