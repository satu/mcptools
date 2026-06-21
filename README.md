# mcptools — DECOMMISSIONED

This repository is **archived and no longer maintained.**

It used to host a small collection of [Model Context Protocol](https://modelcontextprotocol.io)
(MCP) tools. The last remaining tool was the **Trello Asset Downloader**
(`download_trello_asset`), which downloaded authenticated attachments from
Trello cards.

That functionality has been **subsumed by the `trello` CLI in the trellm repo**
(`trellm/trello_cli.py` → `trello download <url> <output_path>`). The CLI's
implementation is a direct port of this MCP tool, so the tool here is redundant.

With no tools left to serve, the repository has been gutted and archived. The
full source — every tool that ever lived here, plus the regression guards that
documented the ones removed earlier — remains available in the git history.

Decommissioned per Trello card `6a386049` (2026-06-21).
