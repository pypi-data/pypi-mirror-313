"""Configuration settings for the arXiv MCP server."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Server configuration settings."""

    APP_NAME: str = "arxiv-mcp-server"
    APP_VERSION: str = "0.2.3"
    MAX_RESULTS: int = 50
    BATCH_SIZE: int = 20
    REQUEST_TIMEOUT: int = 60
    STORAGE_PATH: str = "/Users/josephblazick/.arxiv-mcp-server/papers"
    model_config = SettingsConfigDict(extra="allow")
