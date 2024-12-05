from .message import Message
from .toolcall import ToolCall

class Assistant(Message):
    def __init__(self, content: str, tool_calls=[], tool_result=None):
        super().__init__("assistant", content)

        self.data["tool_calls"] = tool_calls
        self.data["tool_result"] = tool_result
    
    def to_json(self):
        a = super().to_json()

        if self.data["tool_calls"]:
            # Convert to OpenAI tool call format
            # Convert any dict tool calls to ToolCall objects
            if any(isinstance(t, dict) for t in self.data["tool_calls"]):
                self.data["tool_calls"] = [
                    t if not isinstance(t, dict) else ToolCall.from_dict(t)
                    for t in self.data["tool_calls"]
                ]
            a["tool_calls"] = [t.to_json() for t in self.data["tool_calls"]]

        if self.data["tool_result"]:
            a["tool_result"] = self.data["tool_result"]

        return a