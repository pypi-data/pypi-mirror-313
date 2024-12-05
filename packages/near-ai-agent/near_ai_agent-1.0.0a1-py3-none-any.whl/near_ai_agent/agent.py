from near_ai_agent.environment import NearAIEnvironment
from near_ai_agent.tasks import fetch_user_info, provide_weather
import json

class NearAIAgent:
    def __init__(self, config_path="near_ai_agent/config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.name = self.config.get("agent_name", "UnnamedAgent")
        self.version = self.config.get("version", "0.1.0")
        self.default_tasks = self.config.get("default_tasks", {})
        self.environment = NearAIEnvironment()

    def handle_task(self, task, *args):
        """
        Execute a task and manage context/output using the NEAR AI API.
        """
        if task in self.default_tasks:
            return self.environment.output(self.default_tasks[task])
        elif task == "fetch_user_info":
            user_info = fetch_user_info(*args)
            self.environment.set_context("last_user", user_info)
            return self.environment.output(f"User info: {user_info}")
        elif task == "provide_weather":
            weather_info = provide_weather(*args)
            return self.environment.output(f"Weather: {weather_info}")
        else:
            return self.environment.output(f"Task '{task}' not recognized.")

    def run(self):
        """
        Interactive mode for testing tasks.
        """
        print(f"Running {self.name} v{self.version}")
        while True:
            task = input("Enter task: ")
            if task.lower() == "exit":
                print("Exiting...")
                break
            args = input("Enter arguments (comma-separated): ").split(",")
            response = self.handle_task(task, *args)
            print(f"Response: {response}")
