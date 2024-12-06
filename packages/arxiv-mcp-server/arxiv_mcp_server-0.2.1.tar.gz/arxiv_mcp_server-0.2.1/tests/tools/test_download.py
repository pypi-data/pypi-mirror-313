"""Tests for paper download functionality."""

import pytest
import json
from unittest.mock import patch, MagicMock
import arxiv
from arxiv_mcp_server.tools.download import handle_download

@pytest.mark.asyncio
async def test_download_new_paper(mock_client, mock_paper, temp_storage_path):
    """Test downloading a new paper."""
    with patch('arxiv.Client', return_value=mock_client), \
         patch('arxiv_mcp_server.resources.storage.PaperStorage.store_paper', return_value=True):
        
        result = await handle_download({
            "paper_id": "2103.12345"
        })
        
        content = json.loads(result[0].text)
        assert content["status"] == "success"
        assert content["resource_uri"] == "arxiv://2103.12345"

@pytest.mark.asyncio
async def test_download_existing_paper(mock_client, temp_storage_path):
    """Test attempting to download an already stored paper."""
    with patch('arxiv.Client', return_value=mock_client), \
         patch('arxiv_mcp_server.resources.storage.PaperStorage.has_paper', return_value=True):
        
        result = await handle_download({
            "paper_id": "2103.12345"
        })
        
        content = json.loads(result[0].text)
        assert content["status"] == "success"
        assert "already available" in content["message"]

@pytest.mark.asyncio
async def test_download_nonexistent_paper():
    """Test downloading a paper that doesn't exist."""
    empty_client = MagicMock(spec=arxiv.Client)
    empty_client.results = MagicMock(return_value=[])
    
    with patch('arxiv.Client', return_value=empty_client):
        result = await handle_download({
            "paper_id": "nonexistent"
        })
        
        content = json.loads(result[0].text)
        assert content["status"] == "error"
        assert "not found" in content["message"]

@pytest.mark.asyncio
async def test_download_failure(mock_client):
    """Test handling download failures."""
    with patch('arxiv.Client', return_value=mock_client), \
         patch('arxiv_mcp_server.resources.storage.PaperStorage.store_paper', return_value=False):
        
        result = await handle_download({
            "paper_id": "2103.12345"
        })
        
        content = json.loads(result[0].text)
        assert content["status"] == "error"
        assert "Failed to download" in content["message"]