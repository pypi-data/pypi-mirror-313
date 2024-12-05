from litellm import completion
import logging
import traceback

from .messages import System, User, Assistant, ToolCall, ToolResult, Dynamic, from_dict, to_dict

class Chat:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.messages = []
        self.tools = {}
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler if no handlers exist
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def __str__(self):
        return f"<Chat(messages={len(self.messages)}, tools={len(self.tools)})>"
    
    def to_dict(self):
        return [to_dict(m) for m in self.messages]
    
    def from_dict(self, dict):
        # Clear existing messages
        self.messages = []
        
        # Convert each dict to a Message, skipping any ToolCall or ToolResult messages
        for m in dict:
            if m["type"] == "ToolResult":
                continue

            if m["type"] == "Assistant":
                m["data"]["tool_calls"] = []

            self.messages.append(from_dict(m))
    
    def dynamic(self):
        """
        Decorator for adding a dynamic message to the chat.
        The decorated function will be called whenever the message needs to be retrieved.
        The function should return a Message object.
        """
        def decorator(func):
            # Find an existing Dynamic message that has no callback and assign the function to it
            # Useful when restoring a chat from a database where the callback cannot be serialized, 
            # and we want to re-assign the dynamic message at the same position in the chat
            for message in self.messages:
                if isinstance(message, Dynamic):
                    if message._callback == None:
                        message._callback = func
                        return func
                    
            # Create a Dynamic message that will call the function when needed
            message = Dynamic(func)
            
            # Add the message to the chat
            self.messages.append(message)
            return func
        
        return decorator

    def tool(self, description: str):
        """
        Decorator for adding a tool to the chat
        """
        def decorator(func):
            self.tools[func.__name__] = {
                "description": description,
                "parameters": func.__annotations__,
                "function": func
            }
            return func
        return decorator
    
    @property
    def tools_to_dict(self):
        """
        Converts the tools to the OpenAI JSON schema format
        """
        tools_dict = []
        for name, tool in self.tools.items():
            tool_dict = {
                "type": "function",
                "function": { 
                    "name": name,
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            
            # Add each parameter as a property
            for param in tool["parameters"]:
                if param == "return": continue
                
                # Get the function annotation for this parameter
                annotation = tool["parameters"][param]
                # Split the annotation string on ": " to get type and description
                if isinstance(annotation, str) and ": " in annotation:
                    param_type, param_desc = annotation.split(": ", 1)

                    # Map param_type to JSON Schema type
                    param_type = {
                        "int": "number",
                        "str": "string",
                        "bool": "boolean",
                        "float": "number"
                    }.get(param_type.lower(), "string")

                    tool_dict["function"]["parameters"]["properties"][param] = {
                        "type": param_type.lower(),
                        "description": param_desc
                    }
                    tool_dict["function"]["parameters"]["required"].append(param)
                    continue
                
                # If no annotation or not in string format, guess string
                tool_dict["function"]["parameters"]["properties"][param] = {
                    "type": "string",
                    "description": annotation
                }
                tool_dict["function"]["parameters"]["required"].append(param)
                
            tools_dict.append(tool_dict)
            
        return tools_dict
    
    @property
    def messages_to_dict(self):
        """
        Converts the messages to the OpenAI message format
        """

        # Filter out any assistant messages with tool calls that don't have corresponding tool results
        filtered_messages = []
        i = 0

        while i < len(self.messages):
            message = self.messages[i]
            
            # If this is an assistant message with tool calls
            if isinstance(message, Assistant) and message.data.get("tool_calls"):
                # Look ahead for tool results for each tool call
                tool_calls = message.data["tool_calls"]
                all_tools_have_results = True
                
                # Check if all tool calls have corresponding results
                for tool_call in tool_calls:
                    found_result = False
                    for j in range(i + 1, len(self.messages)):
                        if isinstance(self.messages[j], ToolResult):
                            if self.messages[j].data.get("tool_call_id") == tool_call.id:
                                found_result = True
                                break
                    if not found_result:
                        all_tools_have_results = False
                        break
                
                # Only keep the message if all its tool calls have results
                if all_tools_have_results:
                    filtered_messages.append(message)
            else:
                filtered_messages.append(message)
            
            i += 1
            
        self.messages = filtered_messages
        return [m.to_json() for m in self.messages if m.to_json() is not None]
    
    def system(self, message: str):
        """
        Adds a system message to the chat
        """
        self.messages.append(System(content=message))
        return self
    
    def user(self, message: str):
        """
        Adds a user message to the chat
        """
        self.messages.append(User(content=message))
        return self
    
    def assistant(self, message: str):
        """
        Adds an assistant message to the chat
        """
        self.messages.append(Assistant(content=message))
        return self
    
    def append(self, message):
        """
        Appends a message to the chat
        """
        if isinstance(message, list):
            self.messages.extend(message)
        else:
            self.messages.append(message)
        return self

    def send(self, message: str):
        """
        Sends a user message to the LLM and automatically handles the response
        """
        self.messages.append(User(content=message))
        return self.ready()
    
    def call_tool(self, tool_call: ToolCall):
        """
        Calls a tool with the given ToolCall object, used internally by the ready() method
        """
        tool_result = self.tools[tool_call.name]["function"](**tool_call.arguments)
        
        self.logger.debug(f"Tool call {tool_call.name} returned")

        self.messages.append(ToolResult(
            content=str(tool_result),
            name=tool_call.name,
            tool_call_id=tool_call.id
        ))

    @property
    def stream(self):
        """
        Whether to stream the response from the LLM
        """
        return self.kwargs.get("stream", False)
    
    def parse_chunk(self, chunk):
        """
        Parses a chunk from the LLM
        """
        pass

    def ready(self):
        """
        Sends the messages to the LLM and handles the response
        """
        responses = []
        iteration = 0 # Used for debugging

        while True:
            iteration += 1
            self.logger.debug(f"This is iteration #{iteration}")

            try: 
                response = completion(
                    messages=self.messages_to_dict,
                    tools=self.tools_to_dict if self.tools else None,
                    **self.kwargs
                )
            except Exception as e:
                self.logger.error(f"Fatal error in completion: {e}")
                self.logger.error(traceback.format_exc())
                raise e
            
            if self.stream:
                for chunk in response:
                    self.parse_chunk(chunk)

            else:
                response = response.json()
                message = response["choices"][0]["message"]

                tool_calls = []
                if "tool_calls" in message:
                    if isinstance(message["tool_calls"], list):
                        # Convert the tool calls to our ToolCall objects
                        tool_calls = [
                            ToolCall(
                                name=t["function"]["name"],
                                arguments=t["function"]["arguments"],
                                id=t["id"]
                            ) for t in message["tool_calls"]
                        ]
 
                # Get the content of the message - some APIs return null, yet 
                # still require an empty string, so we check for that
                content = message["content"] or ""

                self.messages.append(Assistant(
                    content=content, 
                    tool_calls=tool_calls
                ))

                # If there is content, add it to the responses
                if content:
                    responses.append(content)

                # If there are tool calls, execute them
                if tool_calls:
                    self.logger.debug(f"There are {len(tool_calls)} tool calls")
                    # Iterate through each tool call and execute it
                    for tool_call in tool_calls:
                        self.logger.debug(f"Executing tool call {tool_call.name}")

                        # Execute the tool call
                        self.call_tool(tool_call)

                else:
                    # If there are no tool calls, return the responses
                    self.logger.debug("There are no tool calls on this iteration")
                    self.logger.debug(f"Returning {len(responses)} responses")
                    return responses
