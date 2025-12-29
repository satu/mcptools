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
from tmux_manager import tmux_list_windows, tmux_new_window, tmux_rename_window, tmux_send_keys

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
        res = asyncio.run(tmux_new_window.run({"name": "mcp-test", "command": "sleep 10", "keep_open": False}))
        text = get_text(res)
        self.assertIn("Started command", text)

        # Allow tmux to spawn it
        time.sleep(0.5)

        # 3. Rename Window
        print("  - Renaming window to 'mcp-renamed'...")
        res = asyncio.run(tmux_rename_window.run({"new_name": "mcp-renamed", "target_window": "mcp-test"}))
        text = get_text(res)
        self.assertIn("Renamed", text)

        # Verify rename
        windows_res = asyncio.run(tmux_list_windows.run({}))
        windows_text = get_text(windows_res)
        self.assertIn("mcp-renamed", windows_text, "Window should be renamed")

        # 4. Send Keys (Close the window)
        print("  - Sending C-c to close window...")
        res = asyncio.run(tmux_send_keys.run({"target_pane": "mcp-renamed", "keys": "C-c"}))
        text = get_text(res)
        self.assertIn("Sent keys", text)
        
        # Wait for close
        time.sleep(0.5)
        windows_res = asyncio.run(tmux_list_windows.run({}))
        windows_text = get_text(windows_res)
        self.assertNotIn("mcp-renamed", windows_text, "Window should be closed")

if __name__ == "__main__":
    unittest.main()
