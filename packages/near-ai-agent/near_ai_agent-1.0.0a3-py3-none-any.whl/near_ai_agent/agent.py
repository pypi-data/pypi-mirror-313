from typing import Dict, Any, List, Optional
from .environment import NearAIEnvironment
from .tasks import fetch_user_info, provide_weather
import json

class NearAIAgent:
    def __init__(self, env=None, config_path="near_ai_agent/config.json"):
        """
        Initialize the agent with optional NEAR AI environment
        
        Args:
            env: Optional NEAR AI environment object
            config_path: Path to configuration file
        """
        self.environment = NearAIEnvironment(env)
        self._load_config(config_path)
        self.tool_registry = self.environment.get_tool_registry()
        self._register_tools()
        
    def _load_config(self, config_path: str) -> None:
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
            self.name = self.config.get("agent_name", "UnnamedAgent")
            self.version = self.config.get("version", "0.1.0")
            self.system_prompt = self.config.get("system_prompt", {
                "role": "system",
                "content": "You are a helpful AI assistant."
            })
        except FileNotFoundError:
            self.config = {}
            self.name = "UnnamedAgent"
            self.version = "0.1.0"
            self.system_prompt = {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }

    def _register_tools(self) -> None:
        """Register available tools"""
        # Register existing task functions as tools
        self.tool_registry.register_tool(fetch_user_info)
        self.tool_registry.register_tool(provide_weather)
        
        # Register additional tools
        @self.tool_registry.register_tool
        def save_progress(filename: str, content: str) -> str:
            """Save progress to a file"""
            if hasattr(self.environment.env, 'write_file'):
                self.environment.env.write_file(filename, content)
            return f"Progress saved to {filename}"

    def process_message(self, max_iterations: int = 5) -> None:
        """Main message processing loop"""
        iteration = 0
        while iteration < max_iterations:
            messages = self.environment.list_messages()
            if not messages:
                self.environment.request_user_input()
                return

            full_messages = [self.system_prompt] + messages
            tools = self.tool_registry.get_all_tool_definitions()
            
            response = self.environment.completions_and_run_tools(
                messages=full_messages,
                tools=tools,
                model=self.config.get("model", "qwen2p5-72b-instruct"),
                temperature=self.config.get("temperature", 0.7)
            )

            if self._needs_user_input(response):
                self.environment.request_user_input()
                return

            iteration += 1

        self.environment.request_user_input()

    def _needs_user_input(self, response: Dict[str, Any]) -> bool:
        """Check if user input is needed"""
        content = str(response.get("content", "")).lower()
        return any(phrase in content for phrase in [
            "request_user_input",
            "please clarify",
            "could you specify",
            "need more information"
        ])

    def run(self) -> None:
        """Main run loop"""
        print(f"Running {self.name} v{self.version}")
        try:
            while True:
                self.process_message()
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            print(f"Error: {str(e)}")
            raise