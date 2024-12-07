"""Tests for resource management functionality."""

import pytest
import base64
from typing import Union
from unittest.mock import patch
from pathlib import Path
from pydantic import AnyUrl, BaseModel
from arxiv_mcp_server.resources.manager import ResourceManager
from arxiv_mcp_server.config import Settings

settings = Settings()


class URIModel(BaseModel):
    uri: AnyUrl


def make_uri(path: str) -> AnyUrl:
    return URIModel(uri=path).uri


def normalize_uri(uri: Union[str, AnyUrl]) -> str:
    return str(uri).rstrip("/")


@pytest.mark.asyncio
async def test_list_resources():
    manager = ResourceManager()
    with patch(
        "arxiv_mcp_server.resources.storage.PaperStorage.list_papers",
        return_value=["2103.12345"],
    ):
        resources = await manager.list_resources()
        assert len(resources) == 1
        resource = resources[0]
        expected_path = Path(settings.STORAGE_PATH) / "2103.12345.pdf"
        assert normalize_uri(resource.uri) == normalize_uri(f"file://{expected_path}")
        assert resource.mimeType == "application/pdf"


@pytest.mark.asyncio
async def test_read_resource(mock_pdf_content):
    manager = ResourceManager()
    paper_path = Path(settings.STORAGE_PATH) / "2103.12345.pdf"
    uri = make_uri(f"file://{paper_path}")

    with patch(
        "arxiv_mcp_server.resources.storage.PaperStorage.get_paper_content",
        return_value=mock_pdf_content,
    ):
        contents = await manager.read_resource(uri)
        assert len(contents) == 1
        content = contents[0]
        decoded_content = base64.b64decode(content.blob)
        assert decoded_content == mock_pdf_content
        assert content.mimeType == "application/pdf"
        assert normalize_uri(content.uri) == normalize_uri(uri)


@pytest.mark.asyncio
async def test_read_resource_uri_parsing():
    manager = ResourceManager()
    base_path = Path(settings.STORAGE_PATH) / "2412.02674v1.pdf"
    test_uris = [make_uri(f"file://{base_path}"), make_uri(f"file:///{base_path}")]
    test_content = b"test"

    for uri in test_uris:
        with patch(
            "arxiv_mcp_server.resources.storage.PaperStorage.get_paper_content",
            return_value=test_content,
        ):
            contents = await manager.read_resource(uri)
            assert len(contents) == 1
            content = contents[0]
            decoded_content = base64.b64decode(content.blob)
            assert decoded_content == test_content
            assert normalize_uri(content.uri) == normalize_uri(uri)


@pytest.mark.asyncio
async def test_read_nonexistent_resource():
    manager = ResourceManager()
    paper_path = Path(settings.STORAGE_PATH) / "nonexistent.pdf"
    uri = make_uri(f"file://{paper_path}")

    with patch(
        "arxiv_mcp_server.resources.storage.PaperStorage.get_paper_content",
        return_value=None,
    ):
        with pytest.raises(ValueError, match="Resource not found"):
            await manager.read_resource(uri)
