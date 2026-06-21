"""Inventory guard: the repo's live MCP tools are exactly what the docs claim.

This answers the recurring question "what MCP tools do we have in the repo?"
(Trello card 6a386049) and locks the answer so it can't silently drift:

  * Exactly one live MCP tool exists -- ``download_trello_asset`` -- discovered
    by scanning the source for ``@mcp.tool()``-decorated functions.
  * Every live tool is documented in README.md, CLAUDE.md, and GEMINI.md.

If a tool is added or removed, this test fails until the inventory below and
the docs are updated to match. Complements the ``test_no_*.py`` guards, which
keep *removed* tools from creeping back in.
"""

import os
import re
import unittest

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

# The complete, intended set of live MCP tools (function names decorated with
# ``@mcp.tool()``). Update this -- and the docs -- when tools change.
_EXPECTED_TOOLS = {"download_trello_asset"}

_DOCS = ("README.md", "CLAUDE.md", "GEMINI.md")

# Directories that never hold first-party tool source.
_SKIP_DIRS = {"venv", ".venv", "__pycache__", ".git", "node_modules"}

# ``@mcp.tool(...)`` (optionally with args) immediately above a ``def`` line.
_TOOL_DECORATOR = re.compile(
    r"@mcp\.tool\([^)]*\)\s*\n\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",
)


def _read(relpath):
    with open(os.path.join(_REPO_ROOT, relpath), encoding="utf-8") as f:
        return f.read()


def _discover_tools():
    """Return the set of ``@mcp.tool()``-decorated function names in the repo."""
    found = set()
    for dirpath, dirnames, filenames in os.walk(_REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
        for name in filenames:
            if not name.endswith(".py"):
                continue
            text = _read(os.path.relpath(os.path.join(dirpath, name), _REPO_ROOT))
            found.update(_TOOL_DECORATOR.findall(text))
    return found


class TestToolInventory(unittest.TestCase):
    def test_live_tools_match_expected(self):
        self.assertEqual(
            _discover_tools(),
            _EXPECTED_TOOLS,
            "The set of @mcp.tool() functions changed. Update _EXPECTED_TOOLS "
            "and the docs (README.md/CLAUDE.md/GEMINI.md) to match.",
        )

    def test_each_tool_is_documented(self):
        for doc in _DOCS:
            text = _read(doc)
            for tool in _EXPECTED_TOOLS:
                self.assertIn(
                    tool, text, f"{doc} should document the {tool!r} tool"
                )


if __name__ == "__main__":
    unittest.main()
