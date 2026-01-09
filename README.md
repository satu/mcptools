# MCP Tools Collection

This repository contains a collection of Model Context Protocol (MCP) tools designed for use with Claude Code, Gemini CLI, and other MCP-compatible clients.

## Available Tools

1.  **Trello Asset Downloader**: Downloads authenticated assets (attachments) from Trello cards. This tool was created to complement `@delorenj/mcp-server-trello`, which currently lacks support for downloading images and other attachments from cards.
2.  **Tmux Manager**: Manages tmux windows and panes (list, create, rename, send keys) directly from the agent.

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
    *   Create launcher scripts in `~/bin/` (e.g., `mcp-trello-downloader`, `mcp-tmux-manager`).

    **Note**: Ensure `~/bin` is in your system's `PATH`.

## Configuration

### Claude Code

Use the `claude mcp add` command with **absolute paths** (not `$HOME` or `~`):

```bash
# Tmux Manager
claude mcp add tmux-manager /home/YOUR_USER/bin/mcp-tmux-manager --scope user

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

#### Tmux Manager

This tool interacts with your local `tmux` sessions.

```json
"mcpServers": {
  "tmux-manager": {
    "command": "$HOME/bin/mcp-tmux-manager"
  }
}
```

**Requirements:**
*   The `tmux` executable must be in the system `PATH`.

**Session Management:**
*   **Inside Tmux**: If the tool is running inside a tmux session, it operates on that session.
*   **Outside Tmux**: It automatically creates and manages a dedicated session (`mcptools-session`), cleaning it up on exit if it created it.

## Usage

### Trello Downloader
Ask the agent to download files from Trello URLs.
*   "Download the attachment from this Trello card URL."
*   "Get the image from the comment on card [ID]."

### Tmux Manager
Ask the agent to manage your workspace.
*   "List all open tmux windows."
*   "Create a new window named 'server' and run 'npm start'."
*   "Rename the current window to 'logs'."
*   "Split the current window vertically and run 'htop'."
*   "Capture the last 20 lines from the 'build' pane."
*   "Select window '1'."
*   "Kill the window named 'temp'."

## Development

The project uses `fastmcp` to define tools.

*   **Trello Tool**: `download_trello_asset/download_trello_asset.py`
*   **Tmux Tool**: `tmux_manager/tmux_manager.py`

### Running Tests
Unit tests are available for all tools.

```bash
# Run all tests (requires tmux for integration tests)
./venv/bin/python3 -m unittest discover -p "test_*.py"
```