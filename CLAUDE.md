# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of Model Context Protocol (MCP) tools built with Python and `fastmcp`. Currently includes:
- **Trello Asset Downloader** (`download_trello_asset/`) - Downloads authenticated attachments from Trello
- **Tmux Manager** (`tmux_manager/`) - Manages tmux windows and panes from an MCP client
- **Audio Transcriber** (`audio_transcriber/`) - Transcribes audio files using OpenAI Whisper

## Commands

```bash
# Run all tests
./venv/bin/python3 -m unittest discover -p "test_*.py"

# Run a specific test file
./venv/bin/python3 -m unittest download_trello_asset/test_trello_downloader.py
./venv/bin/python3 -m unittest tmux_manager/test_tmux_manager_unit.py
./venv/bin/python3 -m unittest audio_transcriber/test_audio_transcriber.py

# Run an MCP server directly (for testing)
./venv/bin/python3 download_trello_asset/download_trello_asset.py
./venv/bin/python3 tmux_manager/tmux_manager.py
./venv/bin/python3 audio_transcriber/audio_transcriber.py

# Install tools locally (creates launchers in ~/bin/)
./install.sh
```

## Architecture

Each tool is a standalone MCP server in its own subdirectory:
- Main tool logic: `<tool>/tool_name.py`
- Tests: `<tool>/test_*.py`
- Tool-specific requirements: `<tool>/requirements.txt`

Tools are defined using the `@mcp.tool()` decorator from `fastmcp`. Each tool module creates a `FastMCP` instance and runs as an MCP server.

### Tmux Manager Session Handling

The tmux manager has two modes:
1. **Inside tmux** (`TMUX` env var present): Operates on the current session
2. **Outside tmux**: Creates/uses a dedicated session (`mcptools-session`) with automatic cleanup via `atexit`

The `resolve_target()` function handles target qualification for both modes.

## Environment Variables

Trello tool requires:
- `TRELLO_API_KEY`
- `TRELLO_TOKEN`

Audio transcriber:
- `WHISPER_MODEL` (optional, defaults to `base`)
- Requires `ffmpeg` to be installed on the system
