#!/bin/bash
set -e

INSTALL_DIR="$HOME/.local/share/mcptools/trello-downloader"
BIN_DIR="$HOME/bin"
SCRIPT_NAME="mcp-trello-downloader"

echo "Installing Trello Asset Downloader..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy files
echo "Copying files to $INSTALL_DIR..."
cp download_trello_asset/download_trello_asset.py "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"

# Set up virtual environment
echo "Setting up virtual environment..."
if [ ! -d "$INSTALL_DIR/venv" ]; then
    python3 -m venv "$INSTALL_DIR/venv"
fi

# Install dependencies
echo "Installing dependencies..."
"$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

# Create launcher script
echo "Creating launcher in $BIN_DIR/$SCRIPT_NAME..."
cat > "$BIN_DIR/$SCRIPT_NAME" << EOF
#!/bin/bash
exec "$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/download_trello_asset.py" "\$@"
EOF

chmod +x "$BIN_DIR/$SCRIPT_NAME"

# --- Tmux Manager Installation ---
TMUX_INSTALL_DIR="$HOME/.local/share/mcptools/tmux-manager"
TMUX_SCRIPT_NAME="mcp-tmux-manager"

echo ""
echo "Installing Tmux Manager..."

# Create directories
mkdir -p "$TMUX_INSTALL_DIR"

# Copy files
echo "Copying files to $TMUX_INSTALL_DIR..."
cp tmux_manager/tmux_manager.py "$TMUX_INSTALL_DIR/"
cp tmux_manager/requirements.txt "$TMUX_INSTALL_DIR/"

# Set up virtual environment
echo "Setting up virtual environment for Tmux Manager..."
if [ ! -d "$TMUX_INSTALL_DIR/venv" ]; then
    python3 -m venv "$TMUX_INSTALL_DIR/venv"
fi

# Install dependencies
echo "Installing dependencies..."
"$TMUX_INSTALL_DIR/venv/bin/pip" install -r "$TMUX_INSTALL_DIR/requirements.txt"

# Create launcher script
echo "Creating launcher in $BIN_DIR/$TMUX_SCRIPT_NAME..."
cat > "$BIN_DIR/$TMUX_SCRIPT_NAME" << EOF
#!/bin/bash
exec "$TMUX_INSTALL_DIR/venv/bin/python" "$TMUX_INSTALL_DIR/tmux_manager.py" "\$@"
EOF

chmod +x "$BIN_DIR/$TMUX_SCRIPT_NAME"

# --- Audio Transcriber Installation ---
AUDIO_INSTALL_DIR="$HOME/.local/share/mcptools/audio-transcriber"
AUDIO_SCRIPT_NAME="mcp-audio-transcriber"

echo ""
echo "Installing Audio Transcriber..."

# Create directories
mkdir -p "$AUDIO_INSTALL_DIR"

# Copy files
echo "Copying files to $AUDIO_INSTALL_DIR..."
cp audio_transcriber/audio_transcriber.py "$AUDIO_INSTALL_DIR/"
cp audio_transcriber/requirements.txt "$AUDIO_INSTALL_DIR/"

# Set up virtual environment
echo "Setting up virtual environment for Audio Transcriber..."
if [ ! -d "$AUDIO_INSTALL_DIR/venv" ]; then
    python3 -m venv "$AUDIO_INSTALL_DIR/venv"
fi

# Install dependencies
echo "Installing dependencies (this may take a while for Whisper)..."
"$AUDIO_INSTALL_DIR/venv/bin/pip" install -r "$AUDIO_INSTALL_DIR/requirements.txt"

# Create launcher script
echo "Creating launcher in $BIN_DIR/$AUDIO_SCRIPT_NAME..."
cat > "$BIN_DIR/$AUDIO_SCRIPT_NAME" << EOF
#!/bin/bash
exec "$AUDIO_INSTALL_DIR/venv/bin/python" "$AUDIO_INSTALL_DIR/audio_transcriber.py" "\$@"
EOF

chmod +x "$BIN_DIR/$AUDIO_SCRIPT_NAME"

echo ""
echo "Installation complete!"
echo "Tools have been installed to $BIN_DIR"
echo ""
echo "To configure Gemini CLI, add the following to your settings.json:"
echo "---------------------------------------------------------------"
echo '"mcpServers": {'
echo '  "trello-downloader": {'
echo '    "command": "$HOME/bin/'$SCRIPT_NAME'",'
echo '    "env": {'
echo '      "TRELLO_API_KEY": "your_trello_api_key",'
echo '      "TRELLO_TOKEN": "your_trello_api_token"'
echo '    }'
echo '  },'
echo '  "tmux-manager": {'
echo '    "command": "$HOME/bin/'$TMUX_SCRIPT_NAME'"'
echo '  },'
echo '  "audio-transcriber": {'
echo '    "command": "$HOME/bin/'$AUDIO_SCRIPT_NAME'",'
echo '    "env": {'
echo '      "TRELLO_API_KEY": "your_trello_api_key",'
echo '      "TRELLO_TOKEN": "your_trello_api_token",'
echo '      "WHISPER_MODEL": "base"'
echo '    }'
echo '  }'
echo '}'
echo "---------------------------------------------------------------"
echo "Make sure $BIN_DIR is in your PATH."
