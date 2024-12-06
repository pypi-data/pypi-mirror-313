import asyncio
from typing import Any
from datetime import datetime
import ntplib
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Default NTP server
DEFAULT_NTP_SERVER = 'pool.ntp.org'

app = Server("mcp-simple-timeserver")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_time",
            description="Returns the current local time and timezone information from the current client. An AI can thus know what time it is at your human interlocutor location.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_utc",
            description="Returns accurate UTC time from an NTP server.",
            inputSchema={
                "type": "object",
                "properties": {
                    "server": {
                        "type": "string",
                        "description": "NTP server address (default: pool.ntp.org)"
                    }
                },
                "additionalProperties": False
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "get_time":
        local_time = datetime.now()
        timezone = str(datetime.now().astimezone().tzinfo)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
        return [TextContent(
            type="text",
            text=f"Current Time: {formatted_time}\nTimezone: {timezone}"
        )]
    elif name == "get_utc":
        try:
            ntp_client = ntplib.NTPClient()
            server = arguments.get("server", DEFAULT_NTP_SERVER)
            response = ntp_client.request(server, version=3)
            utc_time = datetime.utcfromtimestamp(response.tx_time)
            formatted_time = utc_time.strftime("%Y-%m-%d %H:%M:%S")
            used_server = f" (using {server})" if server != DEFAULT_NTP_SERVER else ""
            return [TextContent(
                type="text",
                text=f"Current UTC Time{used_server}: {formatted_time}"
            )]
        except ntplib.NTPException as e:
            return [TextContent(
                type="text",
                text=f"Error getting NTP time: {str(e)}"
            )]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, write_stream, app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())