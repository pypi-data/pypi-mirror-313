class Document:
    def __init__(self, file_handle):
        self.file_handle = file_handle

    def __str__(self):
        return f"<Document(file_handle={self.file_handle})>"
    
    @property
    def read(self):
        self.file_handle.seek(0)
        return self.file_handle.read()
    
    def to_json(self):
        return {
            "type": "input_document",
            "input_document": {
                "data": self.read,
                "format": self.format
            }
        }