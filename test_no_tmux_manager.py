"""Regression guard: the dead tmux-manager MCP server stays removed.

The Tmux Manager MCP server was removed (Trello card 6a385323): it was a thin
``fastmcp`` wrapper over ``tmux`` subcommands, registered user-globally in
``~/.claude.json`` so it loaded into *every* Claude session for almost no use.
Its registration was removed (``claude mcp remove "tmux-manager" -s user``) and
it was replaced by an on-demand ``tmux`` skill in the trellm repo
(``skills/tmux/SKILL.md``) that reports every operation through the ``tmux`` CLI.

These tests fail if the tool's source or its install/doc references creep back
in, so a future edit can't silently resurrect the dead MCP server. (Mirrors
``test_no_audio_transcriber.py``.)
"""

import os
import unittest

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def _read(relpath):
    with open(os.path.join(_REPO_ROOT, relpath), encoding="utf-8") as f:
        return f.read()


class TestTmuxManagerRemoved(unittest.TestCase):
    def test_source_directory_is_gone(self):
        self.assertFalse(
            os.path.exists(os.path.join(_REPO_ROOT, "tmux_manager")),
            "tmux_manager/ should be removed (dead MCP server)",
        )

    def test_install_script_has_no_references(self):
        install = _read("install.sh")
        for needle in ("tmux_manager", "tmux-manager", "Tmux Manager", "mcp-tmux-manager"):
            self.assertNotIn(
                needle, install, f"install.sh should not reference {needle!r}"
            )

    def test_docs_have_no_references(self):
        for doc in ("README.md", "CLAUDE.md"):
            text = _read(doc)
            for needle in ("tmux_manager", "tmux-manager", "Tmux Manager", "mcp-tmux-manager"):
                self.assertNotIn(
                    needle, text, f"{doc} should not reference {needle!r}"
                )


if __name__ == "__main__":
    unittest.main()
