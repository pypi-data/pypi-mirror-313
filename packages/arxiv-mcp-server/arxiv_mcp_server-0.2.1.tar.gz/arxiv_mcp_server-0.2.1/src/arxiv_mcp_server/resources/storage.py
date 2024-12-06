"""Storage management for arXiv papers."""

import os
import aiohttp
import aiofiles
from pathlib import Path
from typing import Optional
from ..config import Settings

class PaperStorage:
    """Manages the storage and retrieval of arXiv papers."""
    
    def __init__(self, storage_path: Optional[str] = None):
        """Initialize the paper storage system."""
        settings = Settings()
        self.storage_path = Path(storage_path or settings.STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def _get_paper_path(self, paper_id: str) -> Path:
        """Get the file path for a paper."""
        return self.storage_path / f"{paper_id}.pdf"
    
    async def store_paper(self, paper_id: str, pdf_url: str) -> bool:
        """Download and store a paper from arXiv."""
        paper_path = self._get_paper_path(paper_id)
        
        if paper_path.exists():
            return True
            
        try:
            async with aiohttp.ClientSession() as session:
                async with await session.get(pdf_url) as response:
                    if response.status != 200:
                        return False
                        
                    content = await response.read()
                    async with aiofiles.open(paper_path, 'wb') as f:
                        await f.write(content)
                        
                    return True
                    
        except Exception:
            if paper_path.exists():
                paper_path.unlink()
            return False
    
    async def get_paper_content(self, paper_id: str) -> Optional[bytes]:
        """Retrieve the content of a stored paper."""
        paper_path = self._get_paper_path(paper_id)
        
        if not paper_path.exists():
            return None
            
        async with aiofiles.open(paper_path, 'rb') as f:
            return await f.read()
    
    async def has_paper(self, paper_id: str) -> bool:
        """Check if a paper is available in storage."""
        return self._get_paper_path(paper_id).exists()
    
    async def list_papers(self) -> list[str]:
        """List all stored paper IDs."""
        return [p.stem for p in self.storage_path.glob("*.pdf")]