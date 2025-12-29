# MCP Tools Collection

This repository contains Model Context Protocol (MCP) tools for use with Gemini CLI and other MCP clients.

## Available Tools

### Trello Asset Downloader
A tool to download authenticated assets from Trello URLs.

## Installation

1.  Make sure you have `python3` installed.
2.  Run the installation script:

    ```bash
    chmod +x install.sh
    ./install.sh
    ```

    This script will:
    *   Create a virtual environment in `~/.local/share/mcptools/trello-downloader`.
    *   Install required dependencies (`fastmcp`).
    *   Create a launcher script at `~/bin/mcp-trello-downloader`.

## Configuration

To use these tools with the Gemini CLI, you need to update your `settings.json` file (usually located at `~/.gemini/settings.json` or similar, depending on your setup).

### Trello Asset Downloader Configuration

Add the following entry to the `mcpServers` object in your `settings.json`:

```json
"mcpServers": {
  "trello-downloader": {
    "command": "~/bin/mcp-trello-downloader",
    "env": {
      "TRELLO_API_KEY": "YOUR_TRELLO_API_KEY",
      "TRELLO_TOKEN": "YOUR_TRELLO_TOKEN"
    }
  }
}
```

**Note:** Replace `~/bin/mcp-trello-downloader` with the full absolute path if `~` expansion is not supported by your client (e.g., `/home/username/bin/mcp-trello-downloader`).

### Getting Trello API Keys

1.  Log in to Trello.
2.  Go to [https://trello.com/app-key](https://trello.com/app-key).
3.  Copy your **Personal Key** (`TRELLO_API_KEY`).
4.  Click the "Token" link manually to generate a **Token** (`TRELLO_TOKEN`).

## Usage

Once configured, the tool will be available to the Gemini agent. You can ask it to "download the attachment from this Trello card URL" or similar commands.
