#!/usr/bin/env python3
import os
import urllib.request
import urllib.error
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Trello Asset Downloader")

@mcp.tool()
def download_trello_asset(url: str, output_path: str) -> str:
    """
    Downloads an authenticated asset from Trello to a local path.
    Requires TRELLO_API_KEY and TRELLO_TOKEN environment variables to be set in the MCP server configuration.
    """
    key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")

    if not key or not token:
        return "Error: TRELLO_API_KEY and TRELLO_TOKEN environment variables must be set."

    try:
        # Ensure directory exists
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        headers = {
            "Authorization": f'OAuth oauth_consumer_key="{key}", oauth_token="{token}"',
            "User-Agent": "Gemini-CLI-Tool"
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as out_file:
                out_file.write(response.read())
        
        return f"Successfully saved to {output_path}"

    except urllib.error.HTTPError as e:
        return f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return f"URL Error: {e.reason}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(show_banner=False)
