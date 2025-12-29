# Project Overview
`mcptools` is a collection of tools exposed via the Model Context Protocol (MCP).

## Current Tools
1.  **Trello Asset Downloader**: For downloading attachments from Trello cards.
2.  **Tmux Manager**: For managing tmux windows and panes from within an MCP environment.

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

### Running
To run the MCP server:
```bash
python3 download_trello_asset/download_trello_asset.py
```

## Tmux Manager
Located in `tmux_manager/tmux_manager.py`.
This tool allows listing windows and creating new windows in the current tmux session.

### Dependencies
- Python 3
- `fastmcp`
- `tmux` (must be installed and running)

### Functionality
- `tmux_list_windows`: Lists all windows in the current session.
- `tmux_new_window`: Opens a new window with a specified command. Can verify if the window should stay open after execution.

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