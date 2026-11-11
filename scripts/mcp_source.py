"""Read a configured aggregate tool over MCP Streamable HTTP."""
import asyncio

import anyio
import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

# Allow room for JSON-RPC metadata and the optional duplicate text block.
MAX_WIRE_BYTES = 4_100_000


class BoundedStream(httpx2.AsyncByteStream):
    def __init__(self, stream):
        self.stream = stream

    async def __aiter__(self):
        remaining = MAX_WIRE_BYTES
        async for chunk in self.stream:
            remaining -= len(chunk)
            if remaining < 0:
                raise httpx2.ReadError("MCP response exceeded its byte limit")
            yield chunk

    async def aclose(self):
        await self.stream.aclose()


class BoundedTransport(httpx2.AsyncHTTPTransport):
    async def handle_async_request(self, request):
        response = await super().handle_async_request(request)
        if response.headers.get("Content-Encoding", "identity").lower() != "identity":
            await response.aclose()
            raise httpx2.ReadError("MCP response must use identity encoding")
        response.stream = BoundedStream(response.stream)
        return response


async def call_aggregate(url, tool, arguments, headers):
    async with httpx2.AsyncClient(
        headers={**headers, "Accept-Encoding": "identity"},
        timeout=5.0,
        transport=BoundedTransport(),
    ) as http_client:
        transport = streamable_http_client(url, http_client=http_client, max_sse_event_size=MAX_WIRE_BYTES)
        with anyio.fail_after(15):
            async with Client(transport, read_timeout_seconds=5) as client:
                return await client.call_tool(tool, arguments)


def fetch_mcp(config, headers):
    try:
        result = asyncio.run(call_aggregate(config["url"], config["tool"], config.get("arguments", {}), headers))
    except Exception:
        raise ValueError("MCP source could not be reached or its tool call failed") from None
    if result.is_error:
        raise ValueError("MCP tool reported an error")
    if not isinstance(result.structured_content, dict):
        raise ValueError("MCP tool must return a structured JSON object")
    return result.structured_content
