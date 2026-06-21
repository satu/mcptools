# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of Model Context Protocol (MCP) tools built with Python and `fastmcp`. Currently includes:
- **Trello Asset Downloader** (`download_trello_asset/`) - Downloads authenticated attachments from Trello

Some tools that used to live here have been removed and are kept dead by
`test_no_*.py` regression guards (see those files' docstrings for what and why).

## Commands

```bash
# Run all tests
./venv/bin/python3 -m unittest discover -p "test_*.py"

# Run a specific test file
./venv/bin/python3 -m unittest download_trello_asset/test_trello_downloader.py

# Run an MCP server directly (for testing)
./venv/bin/python3 download_trello_asset/download_trello_asset.py

# Install tools locally (creates launchers in ~/bin/)
./install.sh
```

## Architecture

Each tool is a standalone MCP server in its own subdirectory:
- Main tool logic: `<tool>/tool_name.py`
- Tests: `<tool>/test_*.py`
- Tool-specific requirements: `<tool>/requirements.txt`

Tools are defined using the `@mcp.tool()` decorator from `fastmcp`. Each tool module creates a `FastMCP` instance and runs as an MCP server.

## Environment Variables

Trello tool requires:
- `TRELLO_API_KEY`
- `TRELLO_TOKEN`
