# ArXiv MCP Server 📚 

[![Stars](https://img.shields.io/github/stars/blazickjp/arxiv-mcp-server?style=social)](https://github.com/blazickjp/arxiv-mcp-server/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/blazickjp/arxiv-mcp-server/workflows/Tests/badge.svg)](https://github.com/blazickjp/arxiv-mcp-server/actions)

> 🔍 Empower AI models with direct access to academic research through an elegant MCP interface.

The ArXiv MCP Server bridges the gap between AI models and academic research by providing a sophisticated interface to arXiv's extensive research repository. This server enables AI assistants to perform precise paper searches and access full paper content, enhancing their ability to engage with scientific literature.

<div align="center">
  
🌟 **[View Demo](https://github.com/blazickjp/arxiv-mcp-server#demo)** • 
📖 **[Documentation](https://github.com/blazickjp/arxiv-mcp-server/wiki)** • 
🤝 **[Contribute](https://github.com/blazickjp/arxiv-mcp-server/blob/main/CONTRIBUTING.md)** • 
📝 **[Report Bug](https://github.com/blazickjp/arxiv-mcp-server/issues)**

</div>

## ✨ Core Features

- 🔎 **Advanced Search**: Precise queries with date ranges and category filters
- 📥 **Smart Downloads**: Papers become instantly accessible MCP resources
- 🚀 **Async Architecture**: Built for performance and scalability
- 💾 **Local Caching**: Efficient repeated access to frequently used papers

## 🚀 Quick Start

Install using uv:

```bash
uv pip install git+https://github.com/blazickjp/arxiv-mcp-server.git
```

For development:

```bash
# Clone and set up development environment
git clone https://github.com/blazickjp/arxiv-mcp-server.git
cd arxiv-mcp-server

# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install with test dependencies
uv pip install -e ".[test]"
```

### 🔌 Claude Desktop Integration

Add this configuration to your Claude Desktop config file to enable ArXiv paper access:

<details>
<summary>📝 Click to view configuration</summary>

```json
{
    "mcpServers": {
        "arxiv-mcp-server": {
            "command": "uv",
            "args": [
                "run",
                "arxiv-mcp-server",
                "--storage-path", "/path/to/paper/storage",
                "--max-results", "50",
                "--timeout", "30"
            ]
        }
    }
}
```
</details>

Make sure to adjust the storage path and other parameters according to your needs. This configuration enables Claude to search and access ArXiv papers directly through the MCP server.

## 💡 Usage

### Paper Search
Search with precision using multiple criteria:

```python
# Example: Find recent AI papers
result = await call_tool("search_papers", {
    "query": "transformer architecture applications",
    "max_results": 10,
    "date_from": "2023-01-01",
    "categories": ["cs.AI", "cs.LG"],
})

# Response includes detailed metadata
{
    "total_results": 10,
    "papers": [
        {
            "id": "2401.12345",
            "title": "Example Paper Title",
            "authors": ["Author Name"],
            "abstract": "Paper abstract...",
            "categories": ["cs.AI"],
            "published": "2024-01-15T00:00:00Z",
            "resource_uri": "arxiv://2401.12345"
        }
    ]
}
```

### Paper Download
Transform papers into accessible resources:

```python
result = await call_tool("download_paper", {
    "paper_id": "2401.12345"
})
```

## ⚙️ Configuration

Customize through environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `ARXIV_STORAGE_PATH` | Paper storage location | ~/.arxiv-mcp-server/papers |
| `ARXIV_MAX_RESULTS` | Search results limit | 50 |
| `ARXIV_REQUEST_TIMEOUT` | API timeout (seconds) | 30 |

## 🧪 Development

Run the comprehensive test suite:

```bash
python -m pytest
```

The test suite provides:
- ✅ Unit tests for components
- 🔄 Integration tests for MCP compliance
- 🎭 Mock-based service testing
- 📊 Coverage reporting

## 🏗️ Technical Architecture

Our modular design consists of four key components:

1. 🛠️ **Tool Layer**: MCP protocol interface
2. 📚 **Resource Management**: Paper storage and retrieval
3. 🔌 **Service Layer**: ArXiv API integration
4. ⚙️ **Configuration**: Environment-based settings

## 🤝 Contributing

We enthusiastically welcome contributions! To get started:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. ✨ Make your enhancements
4. ✅ Ensure tests pass
5. 📝 Update documentation
6. 🚀 Submit a pull request

## 📦 Dependencies

### Core
- 📚 arxiv>=2.1.0
- 🔌 mcp>=1.0.0
- 🌐 aiohttp>=3.9.1
- ✨ pydantic>=2.8.0
- 📅 python-dateutil>=2.8.2
- 📁 aiofiles>=23.2.1

### Development
- 🧪 pytest>=8.0.0
- ⚡ pytest-asyncio>=0.23.5
- 📊 pytest-cov>=4.1.0
- 🎭 pytest-mock>=3.10.0

## 📄 License

Released under the MIT License. See the LICENSE file for details.

---

<div align="center">

Made with ❤️ by the ArXiv MCP Server Team

If you find this project helpful, please consider giving it a star ⭐

</div>