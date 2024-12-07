"""Resource management for arXiv papers."""

import arxiv
from typing import List
from mcp.server import AnyUrl
import mcp.types as types
from .storage import PaperStorage
import logging

logger = logging.getLogger("arxiv-mcp-server")


class ResourceManager:
    def __init__(self):
        self.storage = PaperStorage()
        self.client = arxiv.Client()

    async def list_resources(self) -> List[types.Resource]:
        paper_ids = await self.storage.list_papers()
        resources = []

        for paper_id in paper_ids:
            search = arxiv.Search(id_list=[paper_id])
            papers = list(self.client.results(search))

            if papers:
                paper = papers[0]
                paper_path = self.storage._get_paper_path(paper_id)
                resources.append(
                    types.Resource(
                        uri=AnyUrl(f"file://{str(paper_path)}"),
                        name=paper.title,
                        description=paper.summary,
                        mimeType="text/markdown",
                    )
                )
        logger.info(f"Found {len(resources)} resources")
        return resources

    async def store_paper(self, paper_id: str, pdf_url: str) -> bool:
        return await self.storage.store_paper(paper_id, pdf_url)
