"""List functionality for the arXiv MCP server."""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types
from ..resources import ResourceManager

list_tool = types.Tool(
    name="list_papers",
    description="List all existing papers available as resources",
    inputSchema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)


async def handle_list_papers(
    arguments: Optional[Dict[str, Any]] = None
) -> List[types.TextContent]:
    """Handle requests to list all stored papers."""
    try:
        resource_manager = ResourceManager()
        resources = await resource_manager.list_resources()

        response_data = {"total_resources": len(resources), "resources": resources}

        return [
            types.TextContent(type="text", text=json.dumps(response_data, indent=2))
        ]

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]
