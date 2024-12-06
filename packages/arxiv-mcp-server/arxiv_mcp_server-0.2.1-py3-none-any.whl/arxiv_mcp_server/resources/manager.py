"""Resource management for arXiv papers."""

import arxiv
from typing import List
import mcp.types as types
from .storage import PaperStorage

class ResourceManager:
    """Manages arXiv paper resources."""
    
    def __init__(self):
        """Initialize the resource manager."""
        self.storage = PaperStorage()
        self.client = arxiv.Client()
    
    async def list_resources(self) -> List[types.Resource]:
        """List available paper resources."""
        paper_ids = await self.storage.list_papers()
        resources = []
        
        for paper_id in paper_ids:
            # Create a single-item search for the specific paper
            search = arxiv.Search(id_list=[paper_id])
            # Use the client instance we created in __init__
            papers = list(self.client.results(search))
            
            if papers:
                paper = papers[0]
                resources.append(
                    types.Resource(
                        uri=f"arxiv://{paper_id}",
                        name=paper.title,
                        description=paper.summary,
                        mimeType="application/pdf"
                    )
                )
        
        return resources
    
    async def read_resource(self, uri: str) -> bytes:
        """Read the content of a paper resource."""
        paper_id = uri.replace("arxiv://", "")
        content = await self.storage.get_paper_content(paper_id)
        
        if content is None:
            raise ValueError(f"Resource not found: {uri}")
            
        return content
    
    async def store_paper(self, paper_id: str, pdf_url: str) -> bool:
        """Store a new paper resource."""
        return await self.storage.store_paper(paper_id, pdf_url)