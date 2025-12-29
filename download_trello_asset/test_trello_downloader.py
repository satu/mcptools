import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import asyncio

# Add current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import download_trello_asset as tool_module

def get_text(result):
    text = ""
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                text += item.text
    return text

class TestTrelloDownloader(unittest.TestCase):
    
    @patch.dict(os.environ, {"TRELLO_API_KEY": "fake_key", "TRELLO_TOKEN": "fake_token"})
    @patch("urllib.request.urlopen")
    def test_download_success(self, mock_urlopen):
        # Mock response
        mock_response = MagicMock()
        mock_response.__enter__.return_value = mock_response
        mock_response.read.return_value = b"fake_image_data"
        mock_urlopen.return_value = mock_response

        # Run tool
        output_path = "/tmp/test_image.png"
        res = asyncio.run(tool_module.download_trello_asset.run({
            "url": "https://trello.com/fake/url",
            "output_path": output_path
        }))
        text = get_text(res)

        # Verify
        self.assertIn("Successfully saved", text)
        
        # Verify file write (mocked by checking logic, but here we actually write to /tmp)
        with open(output_path, "rb") as f:
            content = f.read()
            self.assertEqual(content, b"fake_image_data")
        
        # Cleanup
        if os.path.exists(output_path):
            os.remove(output_path)
            
        print("\nPASSED: Download success test")

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_env_vars(self):
        res = asyncio.run(tool_module.download_trello_asset.run({
            "url": "https://trello.com/fake",
            "output_path": "/tmp/fail.png"
        }))
        text = get_text(res)
        self.assertIn("Error: TRELLO_API_KEY", text)
        print("\nPASSED: Missing env vars test")

if __name__ == "__main__":
    unittest.main()