from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
from . import gauth
import json

class ToolHandler():
    def __init__(self, tool_name: str):
        self.name = tool_name

    def get_tool_description(self) -> Tool:
        raise NotImplementedError()

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        raise NotImplementedError()
    

class GetUserInfoToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_gmail_user_info")

    def get_tool_description(self) -> Tool:
        raise Tool(
           name=self.name,
           description="""Returns the gmail user info.""",
           inputSchema={
               "type": "object",
               "properties": {},
               "required": []
           }
       )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        user_info = gauth.get_user_info()
        return TextContent(
            type="text",
            text=json.dumps(user_info)
        )