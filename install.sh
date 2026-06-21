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
echo '  }'
echo '}'
echo "---------------------------------------------------------------"
echo "Make sure $BIN_DIR is in your PATH."
