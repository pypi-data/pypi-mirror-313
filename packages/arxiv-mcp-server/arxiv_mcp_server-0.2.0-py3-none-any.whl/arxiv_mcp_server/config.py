"""Configuration settings for the arXiv MCP server."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Server configuration settings."""

    APP_NAME: str = "arxiv-mcp-server"
    APP_VERSION: str = "0.2.0"
    MAX_RESULTS: int = 50
    BATCH_SIZE: int = 20
    REQUEST_TIMEOUT: int = 30
    STORAGE_PATH: str = str(Path.home() / ".arxiv-mcp-server" / "papers")

    model_config = SettingsConfigDict(env_prefix="ARXIV_")
