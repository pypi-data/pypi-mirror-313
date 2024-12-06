"""Tests for utility functions."""

from datetime import datetime, timezone
from arxiv_mcp_server.tools.search import _is_within_date_range, _process_paper

def test_is_within_date_range():
    """Test date range validation functionality."""
    date = datetime(2023, 1, 1, tzinfo=timezone.utc)
    start = datetime(2022, 1, 1, tzinfo=timezone.utc)
    end = datetime(2024, 1, 1, tzinfo=timezone.utc)
    
    assert _is_within_date_range(date, start, end) is True
    assert _is_within_date_range(date, None, end) is True
    assert _is_within_date_range(date, start, None) is True
    assert _is_within_date_range(date, None, None) is True
    assert _is_within_date_range(date, datetime(2023, 2, 1, tzinfo=timezone.utc), end) is False
    assert _is_within_date_range(date, start, datetime(2022, 12, 1, tzinfo=timezone.utc)) is False

def test_process_paper(mock_paper):
    """Test paper processing functionality."""
    result = _process_paper(mock_paper)
    
    assert result["id"] == "2103.12345"
    assert result["title"] == "Test Paper"
    assert len(result["authors"]) == 2
    assert result["authors"][0] == "John Doe"
    assert "abstract" in result
    assert "categories" in result
    assert "published" in result
    assert "url" in result
    assert result["resource_uri"] == "arxiv://2103.12345"