class Dynamic:
    def __init__(self, callback):
        self._callback = callback

    def __call__(self):
        if not self._callback:
            raise NotImplementedError("Dynamic message has no callback")
        
        return self._callback()

    def __str__(self):
        return str(self.__call__())
    
    @property
    def content(self):
        return self.__call__().content
    
    @property
    def role(self):
        return self.__call__().role
    
    def to_dict(self):
        return {
            "type": "Dynamic",
            "data": {
                "callback": None # Can't serialize a function
            }
        }
    
    def to_json(self):
        """ Convert to OpenAI message format """
        try:
            return self.__call__().to_json()
        except Exception as e:
            return None
