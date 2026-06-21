# MCP Tools Collection

This repository contains a collection of Model Context Protocol (MCP) tools designed for use with Claude Code, Gemini CLI, and other MCP-compatible clients.

## Available Tools

1.  **Trello Asset Downloader**: Downloads authenticated assets (attachments) from Trello cards. This tool was created to complement `@delorenj/mcp-server-trello`, which currently lacks support for downloading images and other attachments from cards.

> Some tools that used to live here have been removed and are kept dead by
> `test_no_*.py` regression guards (see those files' docstrings + git history
> for what and why).

## Installation

The project provides an automated installation script.

1.  Ensure you have `python3` and `pip` installed.
2.  Run the installation script:

    ```bash
    chmod +x install.sh
    ./install.sh
    ```

    This script will:
    *   Create dedicated virtual environments for each tool in `~/.local/share/mcptools/`.
    *   Install all required dependencies.
    *   Create launcher scripts in `~/bin/` (e.g., `mcp-trello-downloader`).

    **Note**: Ensure `~/bin` is in your system's `PATH`.

## Configuration

### Claude Code

Use the `claude mcp add` command with **absolute paths** (not `$HOME` or `~`):

```bash
# Trello Asset Downloader (with environment variables)
claude mcp add trello-downloader /home/YOUR_USER/bin/mcp-trello-downloader --scope user \
  -e TRELLO_API_KEY=YOUR_TRELLO_API_KEY \
  -e TRELLO_TOKEN=YOUR_TRELLO_TOKEN
```

**Important**: Claude Code does not expand `$HOME` or `~` in paths. Always use absolute paths.

Verify the configuration:
```bash
claude mcp list
```

### Gemini CLI

Add the following to your `settings.json` (typically located at `~/.gemini/settings.json`).

#### Trello Asset Downloader

This tool requires Trello API credentials.

```json
"mcpServers": {
  "trello-downloader": {
    "command": "$HOME/bin/mcp-trello-downloader",
    "env": {
      "TRELLO_API_KEY": "YOUR_TRELLO_API_KEY",
      "TRELLO_TOKEN": "YOUR_TRELLO_TOKEN"
    }
  }
}
```

**Getting Trello API Keys:**
1.  Log in to Trello.
2.  Visit [https://trello.com/app-key](https://trello.com/app-key).
3.  Copy your **Personal Key** (`TRELLO_API_KEY`).
4.  Click the "Token" link manually to generate a **Token** (`TRELLO_TOKEN`).

*Alternatively, the tool supports a `.env` file in its installation directory.*

**Available Tools:**
*   `download_trello_asset(url, output_path)` - Download an authenticated asset from Trello

## Usage

### Trello Downloader
Ask the agent to download files from Trello URLs.
*   "Download the attachment from this Trello card URL."
*   "Get the image from the comment on card [ID]."

## Development

The project uses `fastmcp` to define tools.

*   **Trello Tool**: `download_trello_asset/download_trello_asset.py`

### Running Tests
Unit tests are available for all tools.

```bash
# Run all tests
./venv/bin/python3 -m unittest discover -p "test_*.py"
```
