# MCP Tools Collection

This repository contains a collection of Model Context Protocol (MCP) tools designed for use with Claude Code, Gemini CLI, and other MCP-compatible clients.

## Available Tools

1.  **Trello Asset Downloader**: Downloads authenticated assets (attachments) from Trello cards. This tool was created to complement `@delorenj/mcp-server-trello`, which currently lacks support for downloading images and other attachments from cards.
2.  **Tmux Manager**: Manages tmux windows and panes (list, create, rename, send keys) directly from the agent.
3.  **Audio Transcriber**: Transcribes audio files using OpenAI Whisper. Supports public URLs and local files. For authenticated sources (e.g., Trello), download the file first with the appropriate tool.

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
    *   Create launcher scripts in `~/bin/` (e.g., `mcp-trello-downloader`, `mcp-tmux-manager`, `mcp-audio-transcriber`).

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

# Audio Transcriber (with environment variables)
claude mcp add audio-transcriber /home/YOUR_USER/bin/mcp-audio-transcriber --scope user \
  -e WHISPER_MODEL=base
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

**Available Tools:**
*   `tmux_list_windows()` - List all windows in the current session
*   `tmux_new_window(command, name?, keep_open?)` - Open a new window and run a command
*   `tmux_rename_window(new_name, target_window?)` - Rename a window
*   `tmux_send_keys(keys, target_pane?)` - Send keys to a pane
*   `tmux_get_active_session_info()` - Get info about the current session
*   `tmux_capture_pane(target_pane?, start_line?, end_line?)` - Capture pane content
*   `tmux_split_window(target_pane?, direction?, command?)` - Split a window
*   `tmux_select_window(target_window)` - Switch to a window
*   `tmux_select_pane(target_pane)` - Focus a pane
*   `tmux_kill_window(target_window)` - Close a window
*   `tmux_kill_pane(target_pane?)` - Close a pane

#### Audio Transcriber

This tool transcribes audio files using OpenAI Whisper.

```json
"mcpServers": {
  "audio-transcriber": {
    "command": "$HOME/bin/mcp-audio-transcriber",
    "env": {
      "WHISPER_MODEL": "base"
    }
  }
}
```

**Requirements:**
*   `ffmpeg` must be installed and in the system `PATH` (used by Whisper for audio processing).

**Environment Variables:**
*   `WHISPER_MODEL`: Whisper model size (default: `base`). Options: `tiny`, `base`, `small`, `medium`, `large`.

**Supported Audio Formats:** `.opus`, `.ogg`, `.m4a`, `.mp3`, `.wav`, `.webm`, `.flac`, `.aac`

**Available Tools:**
*   `transcribe_audio(url, language?)` - Transcribe audio from a public URL
*   `transcribe_local_audio(file_path, language?)` - Transcribe a local audio file

**Note:** For authenticated URLs (e.g., Trello attachments), download the file first using the appropriate tool (e.g., `trello-downloader`) and use the local file transcription.

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

### Audio Transcriber
Ask the agent to transcribe audio files.
*   "What does the audio file at [URL] say?"
*   "Transcribe the local audio file at /path/to/recording.mp3"
*   "Transcribe this audio in Italian." (specify language)
*   For Trello voice notes: first download with trello-downloader, then transcribe the local file.

## Development

The project uses `fastmcp` to define tools.

*   **Trello Tool**: `download_trello_asset/download_trello_asset.py`
*   **Tmux Tool**: `tmux_manager/tmux_manager.py`
*   **Audio Tool**: `audio_transcriber/audio_transcriber.py`

### Running Tests
Unit tests are available for all tools.

```bash
# Run all tests (requires tmux for integration tests)
./venv/bin/python3 -m unittest discover -p "test_*.py"
```