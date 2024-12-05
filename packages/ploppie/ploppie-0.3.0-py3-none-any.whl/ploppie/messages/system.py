from .message import Message

class System(Message):
    def __init__(self, content: str):
        super().__init__("system", content)