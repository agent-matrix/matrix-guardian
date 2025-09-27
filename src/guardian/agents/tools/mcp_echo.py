from __future__ import annotations

from typing import Any, Dict


async def mcp_echo_probe(endpoint: str) -> Dict[str, Any]:
    """
    Placeholder for an MCP handshake / 'tool-echo' probe.

    In Stage-1/2 we keep it a no-op that reports 'unimplemented'.
    Swap with a real JSON-RPC check when your MCP client exists.
    """
    return {
        "ok": False,
        "error": "mcp_echo not implemented",
        "endpoint": endpoint,
    }
