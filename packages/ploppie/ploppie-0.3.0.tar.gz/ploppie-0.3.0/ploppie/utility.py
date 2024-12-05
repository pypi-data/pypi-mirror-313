from .chat import Chat

class Utility:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    @property
    def chat(self):
        return Chat(**self.kwargs)
    
    def selector(self, message: str, options: list, attempts: int = 3):
        """
        Prompts the LLM to select one option from a list of choices.
        
        :param message: The prompt or question to ask the LLM
        :type message: str
        :param options: List of valid options the LLM can choose from
        :type options: list
        :param attempts: Number of attempts before raising error, defaults to 3
        :type attempts: int, optional
        
        :returns: The selected option that matches one from the options list
        :rtype: str
        
        :raises ValueError: If no valid selection is made within the allowed attempts
        """
        chat = self.chat
        attempt = 0
        
        while attempt < attempts:
            # Add system message explaining the constraints
            chat.system(f"You must respond with exactly one of these options: {', '.join(options)}")
            chat.system(message)
            
            # Get response from LLM
            responses = chat.ready()
            response = responses[0] if isinstance(responses, list) else responses
            
            # Check if response matches any option
            for option in options:
                if option.lower() == response.lower().strip():
                    return option
            
            attempt += 1
            
            # Add error message for invalid response
            chat.system(f"Invalid selection. Please choose exactly one option from: {', '.join(options)}")
        
        raise ValueError(f"Failed to get valid selection after {attempts} attempts")
