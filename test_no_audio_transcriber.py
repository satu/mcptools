"""Regression guard: the dead audio-transcriber MCP server stays removed.

The audio-transcriber MCP server was removed (Trello card 6a3710f4): its
registration was already gone from ``~/.claude.json`` and no client consumed
it. trellm's voice transcription moved to the Dixit dictation service, with a
local faster-whisper fallback that shells out to the *venv* directly (not this
source), so nothing imports this tool anymore.

These tests fail if the tool's source or its install/doc references creep back
in, so a future edit can't silently resurrect 7.4 GB of dead Whisper deps.
"""

import os
import unittest

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def _read(relpath):
    with open(os.path.join(_REPO_ROOT, relpath), encoding="utf-8") as f:
        return f.read()


class TestAudioTranscriberRemoved(unittest.TestCase):
    def test_source_directory_is_gone(self):
        self.assertFalse(
            os.path.exists(os.path.join(_REPO_ROOT, "audio_transcriber")),
            "audio_transcriber/ should be removed (dead MCP server)",
        )

    def test_install_script_has_no_references(self):
        install = _read("install.sh")
        for needle in ("audio_transcriber", "audio-transcriber", "Audio Transcriber", "WHISPER_MODEL"):
            self.assertNotIn(
                needle, install, f"install.sh should not reference {needle!r}"
            )

    def test_docs_have_no_references(self):
        for doc in ("README.md", "CLAUDE.md"):
            text = _read(doc)
            for needle in ("audio_transcriber", "audio-transcriber", "Audio Transcriber"):
                self.assertNotIn(
                    needle, text, f"{doc} should not reference {needle!r}"
                )


if __name__ == "__main__":
    unittest.main()
