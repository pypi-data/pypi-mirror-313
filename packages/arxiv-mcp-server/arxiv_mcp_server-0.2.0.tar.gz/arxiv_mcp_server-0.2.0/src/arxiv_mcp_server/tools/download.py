"""Download functionality for the arXiv MCP server."""

import arxiv
import json
from typing import Dict, Any, List
import mcp.types as types
from ..resources import ResourceManager

download_tool = types.Tool(
    name="download_paper",
    description="Download a paper and create a resource for it",
    inputSchema={
        "type": "object",
        "properties": {
            "paper_id": {
                "type": "string",
                "description": "arXiv paper ID",
            }
        },
        "required": ["paper_id"],
    },
)

async def handle_download(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle paper download requests."""
    try:
        paper_id = arguments["paper_id"]
        client = arxiv.Client()
        resource_manager = ResourceManager()
        
        # Check if paper already exists
        if await resource_manager.storage.has_paper(paper_id):
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "success",
                    "resource_uri": f"arxiv://{paper_id}",
                    "message": f"Paper {paper_id} is already available as a resource"
                })
            )]
        
        # Fetch paper metadata
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search))
        
        if not papers:
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "message": f"Paper not found: {paper_id}"
                })
            )]
        
        paper = papers[0]
        
        # Download and store the paper
        success = await resource_manager.store_paper(paper_id, paper.pdf_url)
        
        if not success:
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "message": f"Failed to download paper: {paper_id}"
                })
            )]
        
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "status": "success",
                "resource_uri": f"arxiv://{paper_id}",
                "message": f"Paper {paper_id} has been downloaded and is available as a resource"
            })
        )]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "message": f"Error: {str(e)}"
            })
        )]