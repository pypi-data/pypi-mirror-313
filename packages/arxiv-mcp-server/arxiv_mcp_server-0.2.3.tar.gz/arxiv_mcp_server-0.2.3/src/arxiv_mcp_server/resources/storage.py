"""Storage management for arXiv papers."""

from pathlib import Path
from typing import Optional
from ..config import Settings
import arxiv
import pymupdf4llm
import aiofiles
import logging

logger = logging.getLogger("arxiv-mcp-server")


class PaperStorage:
    """Manages the storage and retrieval of arXiv papers."""

    def __init__(self):
        """Initialize the paper storage system."""
        settings = Settings()
        self.storage_path = Path(settings.STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_paper_path(self, paper_id: str) -> Path:
        """Get the absolute file path for a paper."""
        return self.storage_path / f"{paper_id}.md"

    async def store_paper(self, paper_id: str, pdf_url: str) -> bool:
        """Download and store a paper from arXiv."""
        paper_md_path = self._get_paper_path(paper_id)
        paper_pdf_path = paper_md_path.with_suffix(".pdf")

        if paper_md_path.exists():
            return True

        try:
            paper = next(arxiv.Client().results(arxiv.Search(id_list=[paper_id])))
            paper.download_pdf(dirpath=self.storage_path, filename=paper_pdf_path)
            markdown = pymupdf4llm.to_markdown(paper_pdf_path, show_progress=False)

            async with aiofiles.open(paper_md_path, "w") as f:
                await f.write(markdown)

            paper_pdf_path.unlink()
            return True

        except StopIteration:
            raise ValueError(f"Paper with ID {paper_id} not found on arXiv.")

        except arxiv.ArxivError as e:
            raise ValueError(
                f"Error: Failed to download paper {paper_id} from arXiv. Details: {str(e)}"
            )

        except Exception as e:
            raise ValueError(
                f"Error: An unexpected error occurred while storing paper {paper_id}. Details: {str(e)}"
            )

    async def has_paper(self, paper_id: str) -> bool:
        """Check if a paper is available in storage."""
        return self._get_paper_path(paper_id).exists()

    async def list_papers(self) -> list[str]:
        """List all stored paper IDs."""
        logger.info(f"Listing papers in {self.storage_path}")
        paper_ids = [p.stem for p in self.storage_path.glob("*.md")]
        logger.info(f"Found {len(paper_ids)} papers")
        return paper_ids
