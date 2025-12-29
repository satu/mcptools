import sys
import os
import time
import asyncio
import unittest
from unittest.mock import patch

# Add current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the tool functions
# Note: We import the decorated functions directly
from tmux_manager import (
    tmux_list_windows, 
    tmux_new_window, 
    tmux_rename_window, 
    tmux_send_keys,
    tmux_capture_pane,
    tmux_split_window,
    tmux_select_window,
    tmux_select_pane,
    tmux_kill_window,
    tmux_kill_pane
)

def get_text(result):
    text = ""
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                text += item.text
    return text

class TestTmuxManager(unittest.TestCase):

    @patch.dict(os.environ, {}, clear=True)
    def test_not_in_tmux(self):
        """Test that tools report error when TMUX env var is missing."""
        # Ensure TMUX is removed from env for this test
        if "TMUX" in os.environ:
            del os.environ["TMUX"]
            
        print("\n[Test] test_not_in_tmux (Mocked)")
        res = asyncio.run(tmux_list_windows.run({}))
        text = get_text(res)
        self.assertIn("Error: Not running inside a tmux session", text)

    @unittest.skipIf(os.environ.get("TMUX") is None, "Skipping integration tests because not running inside tmux")
    def test_integration_workflow(self):
        """Run the full integration workflow (requires actual tmux)."""
        print("\n[Test] Integration Workflow (Actual Tmux)")

        # 1. List Windows
        print("  - Listing windows...")
        windows_res = asyncio.run(tmux_list_windows.run({}))
        windows_text = get_text(windows_res)
        self.assertIn("active", windows_text, "Should list active window")

        # 2. Create Window
        print("  - Creating window 'mcp-test'...")
        res = asyncio.run(tmux_new_window.run({"name": "mcp-test", "command": "echo 'Hello MCP'; sleep 10", "keep_open": False}))
        text = get_text(res)
        self.assertIn("Started command", text)

        # Allow tmux to spawn it
        time.sleep(1.0)

        # 3. Capture Pane
        print("  - Capturing pane content...")
        res = asyncio.run(tmux_capture_pane.run({"target_pane": "mcp-test"}))
        text = get_text(res)
        self.assertIn("Hello MCP", text)

        # 4. Split Window
        print("  - Splitting window...")
        res = asyncio.run(tmux_split_window.run({"target_pane": "mcp-test", "direction": "vertical", "command": "echo 'Split Pane'"}))
        text = get_text(res)
        self.assertIn("Split window successfully", text)
        time.sleep(0.5)

        # 5. Capture Split Pane Content (the new pane should be active in that window or we target it)
        # Note: Split window makes the new pane the active one in that window usually.
        # But 'mcp-test' might target the window or the original pane depending on resolution.
        # Let's verify we didn't crash.

        # 6. Rename Window
        print("  - Renaming window to 'mcp-renamed'...")
        res = asyncio.run(tmux_rename_window.run({"new_name": "mcp-renamed", "target_window": "mcp-test"}))
        text = get_text(res)
        self.assertIn("Renamed", text)

        # Verify rename
        windows_res = asyncio.run(tmux_list_windows.run({}))
        windows_text = get_text(windows_res)
        self.assertIn("mcp-renamed", windows_text, "Window should be renamed")

        # 7. Kill Window
        print("  - Killing window 'mcp-renamed'...")
        res = asyncio.run(tmux_kill_window.run({"target_window": "mcp-renamed"}))
        
        # Wait for close
        time.sleep(0.5)
        windows_res = asyncio.run(tmux_list_windows.run({}))
        windows_text = get_text(windows_res)
        self.assertNotIn("mcp-renamed", windows_text, "Window should be closed")

if __name__ == "__main__":
    unittest.main()
