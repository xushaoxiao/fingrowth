"""Expose the same invented Argentina aggregate as a read-only MCP tool."""
import argparse
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from .mock_aggregate import aggregate

server = MCPServer("FinGrowth Argentina demo")


@server.tool(annotations=ToolAnnotations(read_only_hint=True, destructive_hint=False))
def registration_credit_aggregate() -> dict[str, Any]:
    """Return the synthetic fixed-window registration-to-credit aggregate."""
    return aggregate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4182)
    args = parser.parse_args()
    server.run(transport="streamable-http", host="127.0.0.1", port=args.port,
               json_response=True, stateless_http=True)
