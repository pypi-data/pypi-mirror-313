from .message import Message
from .system import System
from .user import User
from .assistant import Assistant
from .toolcall import ToolCall
from .toolresult import ToolResult
from .dynamic import Dynamic

import inspect

__all__ = ["Message", "System", "User", "Assistant", "ToolCall", "ToolResult", "Dynamic"]

def to_dict(message):
    """ Convert a Message to a dictionary format, for database storage """
    def encode_value(value):
        if isinstance(value, dict):
            if "..serialized.." in value:
                return value["..serialized.."]
            else:
                return {k: encode_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [encode_value(v) for v in value]
        elif hasattr(value, 'to_dict'):
            return encode_value(value.to_dict())
        
        return value

    return encode_value(message.to_dict())

def from_dict(dict):
    """ Convert a dictionary back to a Message saved from to_dict() """
    type = dict["type"]
    data = dict["data"]

    # Get the class from the type
    message_class = globals()[type]
    
    # Create a new instance with None for all required args
    sig = inspect.signature(message_class.__init__)
    args = {
        param.name: None 
        for param in sig.parameters.values() 
        if param.name != 'self'
    }
    message = message_class(**args)

    # Set the data directly
    message.data = data

    return message