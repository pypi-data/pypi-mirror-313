
import json
import logging
from collections.abc import Sequence
from functools import lru_cache
import subprocess
from typing import Any
import os
from dotenv import load_dotenv
from mcp.server import Server
import threading
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
from . import gauth
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import (
    urlparse,
    parse_qs,
)

class OauthListener(BaseHTTPRequestHandler):
    def do_GET(self):
        print("DO GET")
        url = urlparse(self.path)
        if url.path != "/code":
            self.send_response(404)
            self.end_headers()
            return

        query = parse_qs(url.query)
        if "code" not in query:
            self.send_response(400)
            self.end_headers()
            return
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Auth successful! You can close the tab!".encode("utf-8"))
        self.wfile.flush()

        print(query["code"][0])
        storage = {}
        creds = gauth.get_credentials(authorization_code=query["code"][0], state=storage)
        print("got credentials.", creds)

        t = threading.Thread(target = self.server.shutdown)
        t.daemon = True
        t.start()

        

load_dotenv()

from . import tools

# Load environment variables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-gsuite")

def start_auth_flow():
    oauth_email = os.getenv('GOOGLE_EMAIL')
    if not oauth_email:
        raise RuntimeError("Please set GOOGLE_EMAIL env variable")
    auth_url = gauth.get_authorization_url(oauth_email, state={})
    subprocess.Popen(['open', auth_url])

    # start server for code callback
    server_address = ('', 4100)
    server = HTTPServer(server_address, OauthListener)
    server.serve_forever()


def setup_oauth2():
    credentials = gauth.get_stored_credentials('markus@life-electronic.com')
    if not credentials:
        start_auth_flow()
    else:
        print(f"found oauth2 credentials. User info={gauth.get_user_info(credentials=credentials)}")
        print()

app = Server("mcp-gsuite")

tool_handlers = {}
def add_tool_handler(tool_class: tools.ToolHandler):
    global tool_handlers

    tool_handlers[tool_class.name] = tool_class

def get_tool_handler(name: str) -> tools.ToolHandler | None:
    if name not in tool_handlers:
        return None
    
    return tool_handlers[name]

add_tool_handler(tools.GetUserInfoToolHandler())

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""

    tools = [th.get_tool_description() for th in tool_handlers.values()]
    logging.error(tools)
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls for command line run."""
    
    if not isinstance(arguments, dict):
        raise RuntimeError("arguments must be dictionary")


    tool_handler = get_tool_handler(name)
    if not tool_handler:
        raise ValueError(f"Unknown tool: {name}")

    try:
        return tool_handler.run_tool(arguments)
    except Exception as e:
        logger.error(str(e))
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")


async def main():

    setup_oauth2()
    logging.error("Handled oauth. start MCP server")

    # Import here to avoid issues with event loops
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )



