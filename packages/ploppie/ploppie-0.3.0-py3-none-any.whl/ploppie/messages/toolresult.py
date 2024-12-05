from .message import Message
    
class ToolResult(Message):
    """ Used to return the result of a tool call to the assistant """
    def __init__(self, content: str, name: str, tool_call_id: str):
        super().__init__("tool", content)
        self.data["name"] = name
        self.data["tool_call_id"] = tool_call_id

    def __str__(self):
        return f"<ToolResult(name={self.name}, tool_call_id={self.tool_call_id})>"

    @property
    def name(self):
        return self.data["name"]
    
    @property
    def tool_call_id(self):
        return self.data["tool_call_id"]
    
    def to_json(self):
        # Convert to OpenAI tool result format
        a = super().to_json()
        a["name"] = self.name
        a["tool_call_id"] = self.tool_call_id
        return a