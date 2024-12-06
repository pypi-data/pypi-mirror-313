from typing import Dict, Any, List, Optional
import json

class NearAIEnvironment:
    """
    Environment wrapper that provides compatibility with NEAR AI's environment
    while maintaining backward compatibility.
    """
    def __init__(self, env=None):
        self.env = env  # The NEAR AI environment object if provided
        self.context = {}
        self._load_config()

    def _load_config(self):
        try:
            with open("near_ai_agent/config.json", "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

    def completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Handle completions through NEAR AI or fallback to mock"""
        if self.env:
            return self.env.completion(messages, **kwargs)
        return "Mock completion response"

    def completions_and_run_tools(self, messages: List[Dict[str, str]], tools: List[Dict], **kwargs) -> Dict:
        """Execute completions with tool support"""
        if self.env:
            return self.env.completions_and_run_tools(messages, tools, **kwargs)
        return {"content": "Mock tool execution response"}

    def add_reply(self, message: str) -> None:
        """Add a reply to the conversation"""
        if self.env:
            self.env.add_reply(message)
        else:
            print(f"Mock reply added: {message}")

    def list_messages(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        if self.env:
            return self.env.list_messages()
        return []

    def request_user_input(self) -> None:
        """Request user input"""
        if self.env:
            self.env.request_user_input()
        else:
            print("Mock: Requesting user input")

    def get_tool_registry(self):
        """Get or create tool registry"""
        if self.env:
            return self.env.get_tool_registry()
        return MockToolRegistry()

    def set_context(self, key: str, value: Any) -> None:
        """Set context value"""
        self.context[key] = value

    def get_context(self, key: str) -> Any:
        """Get context value"""
        return self.context.get(key)

class MockToolRegistry:
    """Mock tool registry for local development"""
    def __init__(self):
        self.tools = {}

    def register_tool(self, func):
        self.tools[func.__name__] = func
        return func

    def get_all_tool_definitions(self):
        return [{"name": name, "description": func.__doc__} for name, func in self.tools.items()]