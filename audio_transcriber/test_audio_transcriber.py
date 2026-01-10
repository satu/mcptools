import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import asyncio
import tempfile

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the actual module, not the package
from audio_transcriber import audio_transcriber as tool_module


def get_text(result):
    text = ""
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                text += item.text
    return text


class TestAudioTranscriber(unittest.TestCase):

    def test_get_file_extension(self):
        """Test file extension extraction from URLs."""
        self.assertEqual(tool_module.get_file_extension("https://example.com/audio.mp3"), ".mp3")
        self.assertEqual(tool_module.get_file_extension("https://example.com/audio.opus?token=123"), ".opus")
        self.assertEqual(tool_module.get_file_extension("https://example.com/audio.m4a#fragment"), ".m4a")
        self.assertEqual(tool_module.get_file_extension("https://example.com/noextension"), "")
        print("\nPASSED: File extension extraction test")

    def test_unsupported_format(self):
        """Test that unsupported formats are rejected."""
        res = asyncio.run(tool_module.transcribe_audio.run({
            "url": "https://example.com/document.pdf"
        }))
        text = get_text(res)
        self.assertIn("Unsupported audio format", text)
        print("\nPASSED: Unsupported format test")

    def test_local_file_not_found(self):
        """Test that non-existent local files are handled."""
        res = asyncio.run(tool_module.transcribe_local_audio.run({
            "file_path": "/nonexistent/path/audio.mp3"
        }))
        text = get_text(res)
        self.assertIn("File not found", text)
        print("\nPASSED: Local file not found test")

    def test_local_unsupported_format(self):
        """Test that local files with unsupported formats are rejected."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"test")
            tmp_path = f.name

        try:
            res = asyncio.run(tool_module.transcribe_local_audio.run({
                "file_path": tmp_path
            }))
            text = get_text(res)
            self.assertIn("Unsupported audio format", text)
            print("\nPASSED: Local unsupported format test")
        finally:
            os.remove(tmp_path)

    @patch("urllib.request.urlopen")
    @patch.object(tool_module, "get_model")
    def test_transcribe_url_success(self, mock_get_model, mock_urlopen):
        """Test successful transcription from URL."""
        # Mock URL response
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = b"fake audio data"
        mock_urlopen.return_value = mock_response

        # Mock Whisper model
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {"text": "Hello, this is a test transcription."}
        mock_get_model.return_value = mock_model

        res = asyncio.run(tool_module.transcribe_audio.run({
            "url": "https://example.com/voice_note.mp3"
        }))
        text = get_text(res)

        self.assertEqual(text, "Hello, this is a test transcription.")
        mock_model.transcribe.assert_called_once()
        print("\nPASSED: Transcribe URL success test")

    @patch.object(tool_module, "get_model")
    def test_transcribe_local_success(self, mock_get_model):
        """Test successful transcription from local file."""
        # Create a temp file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(b"fake audio data")
            tmp_path = f.name

        try:
            # Mock Whisper model
            mock_model = MagicMock()
            mock_model.transcribe.return_value = {"text": "Local file transcription."}
            mock_get_model.return_value = mock_model

            res = asyncio.run(tool_module.transcribe_local_audio.run({
                "file_path": tmp_path
            }))
            text = get_text(res)

            self.assertEqual(text, "Local file transcription.")
            mock_model.transcribe.assert_called_once()
            print("\nPASSED: Transcribe local file success test")
        finally:
            os.remove(tmp_path)

    @patch.object(tool_module, "get_model")
    def test_transcribe_with_language(self, mock_get_model):
        """Test transcription with specified language."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(b"fake audio data")
            tmp_path = f.name

        try:
            mock_model = MagicMock()
            mock_model.transcribe.return_value = {"text": "Ciao, questo è un test."}
            mock_get_model.return_value = mock_model

            res = asyncio.run(tool_module.transcribe_local_audio.run({
                "file_path": tmp_path,
                "language": "it"
            }))
            text = get_text(res)

            self.assertEqual(text, "Ciao, questo è un test.")
            # Verify language was passed
            mock_model.transcribe.assert_called_once()
            call_kwargs = mock_model.transcribe.call_args[1]
            self.assertEqual(call_kwargs.get("language"), "it")
            print("\nPASSED: Transcribe with language test")
        finally:
            os.remove(tmp_path)

    @patch.object(tool_module, "get_model")
    def test_empty_transcription(self, mock_get_model):
        """Test handling of empty transcription result."""
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            f.write(b"fake audio data")
            tmp_path = f.name

        try:
            mock_model = MagicMock()
            mock_model.transcribe.return_value = {"text": "   "}
            mock_get_model.return_value = mock_model

            res = asyncio.run(tool_module.transcribe_local_audio.run({
                "file_path": tmp_path
            }))
            text = get_text(res)

            self.assertIn("no speech was detected", text)
            print("\nPASSED: Empty transcription test")
        finally:
            os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
