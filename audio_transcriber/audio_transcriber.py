#!/usr/bin/env python3
import os
import tempfile
import urllib.request
import urllib.error
from fastmcp import FastMCP
from dotenv import load_dotenv
import whisper

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Audio Transcriber")

# Supported audio formats
SUPPORTED_FORMATS = {'.opus', '.ogg', '.m4a', '.mp3', '.wav', '.webm', '.flac', '.aac'}

# Cache the model to avoid reloading on each request
_model = None

def get_model(model_name: str = None):
    """Get or load the Whisper model."""
    global _model
    if model_name is None:
        model_name = os.environ.get("WHISPER_MODEL", "base")
    if _model is None:
        _model = whisper.load_model(model_name)
    return _model


def get_file_extension(url: str) -> str:
    """Extract file extension from URL, handling query parameters and fragments."""
    # Remove query parameters and fragments
    path = url.split('?')[0].split('#')[0]
    ext = os.path.splitext(path)[1].lower()
    return ext


@mcp.tool()
def transcribe_audio(url: str, language: str = None) -> str:
    """
    Transcribes audio from a URL using OpenAI Whisper.

    Args:
        url: URL to the audio file (supports Trello attachment URLs)
        language: Optional language code (e.g., 'en', 'es', 'it'). If not provided, Whisper auto-detects.

    Returns:
        The transcribed text from the audio file.

    Supported formats: .opus, .ogg, .m4a, .mp3, .wav, .webm, .flac, .aac

    For Trello attachments, requires TRELLO_API_KEY and TRELLO_TOKEN environment variables.
    """
    try:
        # Check file extension
        ext = get_file_extension(url)
        if ext and ext not in SUPPORTED_FORMATS:
            return f"Error: Unsupported audio format '{ext}'. Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}"

        # Prepare headers for Trello authentication if needed
        headers = {"User-Agent": "MCP-Audio-Transcriber"}

        if "trello.com" in url or "trello-attachments" in url:
            key = os.environ.get("TRELLO_API_KEY")
            token = os.environ.get("TRELLO_TOKEN")

            if not key or not token:
                return "Error: TRELLO_API_KEY and TRELLO_TOKEN environment variables must be set for Trello URLs."

            headers["Authorization"] = f'OAuth oauth_consumer_key="{key}", oauth_token="{token}"'

        # Download the audio file to a temp location
        with tempfile.NamedTemporaryFile(suffix=ext or '.audio', delete=False) as tmp_file:
            tmp_path = tmp_file.name

            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    tmp_file.write(response.read())
            except urllib.error.HTTPError as e:
                return f"HTTP Error {e.code}: {e.reason}"
            except urllib.error.URLError as e:
                return f"URL Error: {e.reason}"

        try:
            # Load model and transcribe
            model = get_model()

            # Build transcribe options
            options = {}
            if language:
                options["language"] = language

            result = model.transcribe(tmp_path, **options)

            transcription = result["text"].strip()

            if not transcription:
                return "Warning: Audio was transcribed but no speech was detected."

            return transcription

        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def transcribe_local_audio(file_path: str, language: str = None) -> str:
    """
    Transcribes a local audio file using OpenAI Whisper.

    Args:
        file_path: Path to the local audio file
        language: Optional language code (e.g., 'en', 'es', 'it'). If not provided, Whisper auto-detects.

    Returns:
        The transcribed text from the audio file.

    Supported formats: .opus, .ogg, .m4a, .mp3, .wav, .webm, .flac, .aac
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        ext = os.path.splitext(file_path)[1].lower()
        if ext and ext not in SUPPORTED_FORMATS:
            return f"Error: Unsupported audio format '{ext}'. Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}"

        # Load model and transcribe
        model = get_model()

        # Build transcribe options
        options = {}
        if language:
            options["language"] = language

        result = model.transcribe(file_path, **options)

        transcription = result["text"].strip()

        if not transcription:
            return "Warning: Audio was transcribed but no speech was detected."

        return transcription

    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run(show_banner=False)
