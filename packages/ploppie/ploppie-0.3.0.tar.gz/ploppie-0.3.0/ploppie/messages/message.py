from .files import Image, Audio

class Message:
    def __init__(self, role: str, content):
        self.data = {
            "role": role,
            "content": content
        }

    def __str__(self):
        return f"<Message(role={self.role}, content={self.content})>"
    
    @property
    def role(self):
        return self.data["role"]
    
    @property
    def content(self):
        content = []

        if not isinstance(self.data["content"], list):
            self.data["content"] = [self.data["content"]]

        for item in self.data["content"]:
            if isinstance(item, str):
                content.append(item)
            elif type(item) in [Image, Audio]:
                content.append(item.to_json())
            else:
                raise ValueError(f"Unsupported content type: {type(item)}")
            
        # If there is only one item, return it directly
        # OpenAI expects a single item, not a list of one item
        if len(content) == 1:
            if isinstance(content[0], str):
                return content[0]
            
        # If it's a file, though, we'll return the single item list
        
        return content
    
    def to_dict(self):
        """ Convert to a dictionary format, for database storage """
        return {
            "type": self.__class__.__name__,
            "data": self.data
        }

    def to_json(self):
        """ Convert to OpenAI message format """
        return {"role": self.role, "content": self.content}