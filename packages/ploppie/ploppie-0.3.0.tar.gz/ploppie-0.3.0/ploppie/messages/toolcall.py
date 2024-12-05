import json

class ToolCall:
    def __init__(self, name: str, arguments: dict, id: str):
        self.data = {
            "name": name,
            "arguments": arguments,
            "id": id
        }

    def __str__(self):
        return f"<ToolCall(name={self.name}, arguments={self.arguments}, id={self.id})>"
    
    @property
    def name(self):
        return self.data["name"]
    
    @property
    def arguments(self):
        if isinstance(self.data["arguments"], str):
            return json.loads(self.data["arguments"])
        return self.data["arguments"]
    
    @property
    def id(self):
        return self.data["id"]
    
    @classmethod
    def from_dict(cls, dict):
        return cls(**dict["data"])
    
    def to_dict(self):
        return {
            "..serialized..": {
                "type": "ToolCall",
                "data": self.data
            }
        }

    def to_json(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": json.dumps(self.arguments)
            },
            "id": self.id
        }