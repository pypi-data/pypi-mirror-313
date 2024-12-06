"""Tests for resource management functionality."""

import pytest
from unittest.mock import patch
from arxiv_mcp_server.resources.manager import ResourceManager


@pytest.mark.asyncio
async def test_list_resources(temp_storage_path):
    """Test listing available paper resources."""
    manager = ResourceManager()

    with (
        patch(
            "arxiv_mcp_server.resources.storage.PaperStorage.list_papers",
            return_value=["2103.12345"],
        ),
    ):

        resources = await manager.list_resources()
        assert len(resources) == 1
        resource = resources[0]
        assert str(resource.uri) == "arxiv://2103.12345"
        assert (
            resource.name
            == "The Success of AdaBoost and Its Application in Portfolio Management"
        )
        assert resource.description.startswith("We develop")
        assert resource.mimeType == "application/pdf"


@pytest.mark.asyncio
async def test_read_resource(mock_pdf_content, temp_storage_path):
    """Test reading a paper resource."""
    manager = ResourceManager()

    with patch(
        "arxiv_mcp_server.resources.storage.PaperStorage.get_paper_content",
        return_value=mock_pdf_content,
    ):
        content = await manager.read_resource("arxiv://2103.12345")
        assert content == mock_pdf_content


@pytest.mark.asyncio
async def test_read_nonexistent_resource(temp_storage_path):
    """Test reading a non-existent resource."""
    manager = ResourceManager()

    with (
        patch(
            "arxiv_mcp_server.resources.storage.PaperStorage.get_paper_content",
            return_value=None,
        ),
        pytest.raises(ValueError, match="Resource not found"),
    ):
        await manager.read_resource("arxiv://nonexistent")


@pytest.mark.asyncio
async def test_store_paper(temp_storage_path):
    """Test storing a new paper resource."""
    manager = ResourceManager()

    with patch(
        "arxiv_mcp_server.resources.storage.PaperStorage.store_paper", return_value=True
    ):
        success = await manager.store_paper(
            "2103.12345", "https://arxiv.org/pdf/2103.12345"
        )
        assert success
