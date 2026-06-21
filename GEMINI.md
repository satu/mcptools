# Project Overview
`mcptools` is a collection of tools exposed via the Model Context Protocol (MCP).

## Current Tools
1.  **Trello Asset Downloader**: For downloading authenticated attachments from Trello cards.

> Some tools that used to live here have been removed and are kept dead by
> `test_no_*.py` regression guards (see those files' docstrings + git history
> for what and why).

# Tools

## Trello Asset Downloader
Located in `download_trello_asset/download_trello_asset.py`.
This tool allows downloading authenticated assets from Trello URLs.

### Dependencies
- Python 3
- `fastmcp`
- `python-dotenv`

### Configuration
The tool requires Trello API credentials. It supports loading them from environment variables or a `.env` file in the working directory (or installation directory).

Required variables:
- `TRELLO_API_KEY`
- `TRELLO_TOKEN`

### Functionality
- `download_trello_asset(url, output_path)`: Downloads an authenticated asset from a Trello URL to a local path.

### Running
To run the MCP server:
```bash
python3 download_trello_asset/download_trello_asset.py
```

# Installation
The project includes an `install.sh` script to install the tools locally.
```bash
./install.sh
```
This script will:
- Create a virtual environment.
- Install dependencies.
- Create a launcher script in `~/bin`.

# Development Conventions
- The project uses `fastmcp` to define tools.
- Tools are decorated with `@mcp.tool()`.
- Standard Python best practices and error handling are expected.
