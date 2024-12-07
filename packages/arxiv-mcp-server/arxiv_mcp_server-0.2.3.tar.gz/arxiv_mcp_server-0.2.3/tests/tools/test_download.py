"""Tests for paper download functionality using real arXiv papers."""

import json
import pytest
import shutil
from pathlib import Path
from arxiv_mcp_server.tools.download import handle_download
from arxiv_mcp_server.resources.storage import PaperStorage
from arxiv_mcp_server.config import Settings

# Using "Attention Is All You Need" as a stable test paper
STABLE_PAPER_ID = "1706.03762"
settings = Settings()


@pytest.mark.asyncio
async def test_download_paper_lifecycle():
    """Test downloading a real paper from arXiv."""
    # Download paper
    result = await handle_download({"paper_id": STABLE_PAPER_ID})
    content = json.loads(result[0].text)

    assert content["status"] == "success"
    expected_path = Path(settings.STORAGE_PATH) / f"{STABLE_PAPER_ID}.pdf"
    assert content["resource_uri"] == f"file://{expected_path}"
    assert expected_path.exists()
    assert expected_path.stat().st_size > 0


@pytest.mark.asyncio
async def test_download_existing_paper():
    """Test downloading a paper that's already in storage."""

    # First download
    await handle_download({"paper_id": STABLE_PAPER_ID})

    # Try downloading again
    result = await handle_download({"paper_id": STABLE_PAPER_ID})
    content = json.loads(result[0].text)

    expected_path = Path(settings.STORAGE_PATH) / f"{STABLE_PAPER_ID}.pdf"
    assert content["status"] == "success"
    assert content["resource_uri"] == f"file://{expected_path}"
    assert "already available" in content["message"]


@pytest.mark.asyncio
async def test_download_nonexistent_paper(temp_storage_path):
    """Test downloading a non-existent paper ID."""
    result = await handle_download({"paper_id": "0000.00000"})
    content = json.loads(result[0].text)

    assert content["status"] == "error"
    assert "not found" in content["message"]
    assert not (temp_storage_path / "0000.00000.pdf").exists()


def teardown_module(module):
    """Clean up any downloaded papers after tests complete."""
    test_storage = Path("/tmp/arxiv-test-storage")
    if test_storage.exists():
        shutil.rmtree(test_storage)
