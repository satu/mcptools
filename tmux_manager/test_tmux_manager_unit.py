import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys

# Add directory to path to import tmux_manager
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tmux_manager

class TestTmuxExternalLogic(unittest.TestCase):
    
    def setUp(self):
        # Reset the global state
        tmux_manager.CREATED_SESSION = False
        
    @patch.dict(os.environ, {}, clear=True)
    @patch('subprocess.run')
    def test_ensure_session_creates_session_if_missing(self, mock_run):
        # Mock has-session failing (return code 1), then new-session succeeding
        mock_run.side_effect = [
            MagicMock(returncode=1), # has-session -> fails
            MagicMock(returncode=0)  # new-session -> success
        ]
        
        tmux_manager.ensure_session()
        
        self.assertTrue(tmux_manager.CREATED_SESSION)
        # Check calls
        args_list = [c.args[0] for c in mock_run.call_args_list]
        self.assertIn(["tmux", "has-session", "-t", tmux_manager.MCP_SESSION_NAME], args_list)
        self.assertIn(["tmux", "new-session", "-d", "-s", tmux_manager.MCP_SESSION_NAME], args_list)

    @patch.dict(os.environ, {}, clear=True)
    @patch('subprocess.run')
    def test_resolve_target_outside_tmux(self, mock_run):
        # Mock has-session succeeding
        mock_run.return_value = MagicMock(returncode=0)
        
        # Default target
        target = tmux_manager.resolve_target()
        self.assertEqual(target, f"{tmux_manager.MCP_SESSION_NAME}:")
        
        # Explicit target
        target = tmux_manager.resolve_target("1")
        self.assertEqual(target, f"{tmux_manager.MCP_SESSION_NAME}:1")
        
        # Already qualified target
        target = tmux_manager.resolve_target("othersession:1")
        self.assertEqual(target, "othersession:1")

    @patch.dict(os.environ, {"TMUX": "something"})
    def test_resolve_target_inside_tmux(self):
        # Should return raw target
        self.assertIsNone(tmux_manager.resolve_target(None))
        self.assertEqual(tmux_manager.resolve_target("1"), "1")
        
    @patch.dict(os.environ, {}, clear=True)
    @patch('subprocess.run')
    def test_run_tmux_command_invokes_ensure_session(self, mock_run):
        # Mock has-session succeeding, then the command
        mock_run.side_effect = [
            MagicMock(returncode=0), # has-session
            MagicMock(stdout="output", returncode=0) # command
        ]
        
        tmux_manager.run_tmux_command(["list-windows"])
        
        # ensure_session calls has-session
        self.assertEqual(mock_run.call_args_list[0].args[0], ["tmux", "has-session", "-t", tmux_manager.MCP_SESSION_NAME])
        # run_tmux_command calls the command
        self.assertEqual(mock_run.call_args_list[1].args[0], ["tmux", "list-windows"])

if __name__ == '__main__':
    unittest.main()
