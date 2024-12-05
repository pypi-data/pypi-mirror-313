from .message import Message

class User(Message):
    def __init__(self, content: str):
        super().__init__("user", content)