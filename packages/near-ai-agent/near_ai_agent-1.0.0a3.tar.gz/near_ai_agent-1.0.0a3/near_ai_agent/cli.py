# near_ai_agent/cli.py
import argparse
import os
import json
from typing import Optional
from .agent import NearAIAgent
from .environment import NearAIEnvironment
import re

def create_agent(name: str, template: Optional[str] = None) -> None:
    """
    Create a scaffold for a new agent.
    
    Args:
        name: Name of the agent
        template: Optional template to use (basic, advanced, or near)
    """
    # Sanitize the agent name to be a valid Python identifier
    sanitized_name = re.sub(r'\W|^(?=\d)', '_', name)  # Replace non-alphanumeric characters with underscores

    directory = f"./{sanitized_name}"
    if os.path.exists(directory):
        print(f"Directory '{sanitized_name}' already exists. Aborting.")
        return

    os.makedirs(directory)
    
    # Select template configuration
    if template == "near":
        config = {
            "agent_name": sanitized_name,
            "version": "1.0.0",
            "system_prompt": {
                "role": "system",
                "content": "You are a helpful AI assistant that can use tools and process user requests."
            },
            "model": "qwen2p5-72b-instruct",
            "temperature": 0.7
        }
        
        # Create NEAR AI metadata
        metadata = {
            "category": "agent",
            "description": f"A NEAR AI agent named {sanitized_name}",
            "tags": ["python", "assistant"],
            "details": {
                "agent": {
                    "defaults": {
                        "model": "qwen2p5-72b-instruct",
                        "model_max_tokens": 16384,
                        "model_provider": "fireworks",
                        "model_temperature": 0.7
                    }
                }
            },
            "show_entry": True,
            "name": sanitized_name,
            "version": "0.1.0"
        }
        
        with open(f"{directory}/metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
    else:  # basic or advanced template
        config = {
            "agent_name": sanitized_name,
            "version": "1.0.0",
            "default_tasks": {
                "greet": f"Hello! I'm {sanitized_name}, your custom agent.",
                "help": "I can assist with various tasks including file operations and calculations."
            }
        }

    # Write configuration
    with open(f"{directory}/config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Create agent implementation
    agent_code = f"""from near_ai_agent.agent import NearAIAgent

class {sanitized_name.capitalize()}Agent(NearAIAgent):
    def _register_tools(self):
        super()._register_tools()
        
        @self.tool_registry.register_tool
        def custom_action(self, param: str) -> str:
            \"\"\"Example custom tool - replace with your own functionality\"\"\"
            return "Processed {{param}}"

if __name__ == "__main__":
    agent = {sanitized_name.capitalize()}Agent()
    agent.run()
"""
    
    with open(f"{directory}/{sanitized_name}_agent.py", "w") as f:
        f.write(agent_code)
        
    # Create example usage script
    example_code = """import argparse
from near_ai_agent.agent import NearAIAgent
from near_ai_agent.environment import NearAIEnvironment

def main():
    parser = argparse.ArgumentParser(description="Run the agent")
    parser.add_argument("--local", action="store_true", help="Run in local mode")
    parser.add_argument("--env_path", default="/tmp/agent_run", help="Environment path")
    
    args = parser.parse_args()
    
    if args.local:
        env = NearAIEnvironment()  # Creates mock environment
        agent = NearAIAgent(env=env)
    else:
        agent = NearAIAgent()  # For NEAR AI deployment
        
    agent.run()

if __name__ == "__main__":
    main()
"""
    
    with open(f"{directory}/run.py", "w") as f:
        f.write(example_code)

    print(f"""Agent '{sanitized_name}' created successfully in ./{sanitized_name}/
    
Files created:
- {sanitized_name}_agent.py - Main agent implementation
- config.json - Agent configuration
- run.py - Example usage script
{f'- metadata.json - NEAR AI deployment configuration' if template == 'near' else ''}

To run locally:
    python {directory}/run.py --local

For NEAR AI deployment:
    nearai agent interactive {sanitized_name} --local
""")

def run_agent(config_path: str, local: bool = False, env_path: str = "/tmp/agent_run") -> None:
    """
    Run an agent using the provided configuration.
    
    Args:
        config_path: Path to config.json
        local: Whether to run in local mode
        env_path: Path for environment files
    """
    if local:
        env = NearAIEnvironment()  # Creates mock environment
        agent = NearAIAgent(env=env, config_path=config_path)
    else:
        agent = NearAIAgent(config_path=config_path)
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error running agent: {str(e)}")
        raise

def prepare_near(agent_name: str, registry_path: Optional[str] = None) -> None:
    """
    Prepare an agent for NEAR AI deployment.
    
    Args:
        agent_name: Name of the agent
        registry_path: Optional custom registry path
    """
    if not registry_path:
        registry_path = os.path.expanduser(f"~/.nearai/registry/{agent_name}")
    
    if not os.path.exists(f"./{agent_name}"):
        print(f"Agent directory '{agent_name}' not found. Create it first with 'create' command.")
        return
        
    os.makedirs(registry_path, exist_ok=True)
    
    # Copy necessary files
    import shutil
    files_to_copy = [
        f"{agent_name}_agent.py",
        "config.json",
        "metadata.json"
    ]
    
    for file in files_to_copy:
        src = f"./{agent_name}/{file}"
        dst = f"{registry_path}/{file}"
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    print(f"""Agent prepared for NEAR AI deployment in {registry_path}

To deploy:
    nearai registry upload {registry_path}
    
To run:
    nearai agent interactive {agent_name} --local""")

def main() -> None:
    parser = argparse.ArgumentParser(description="CLI for managing NEAR AI agents.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new agent")
    create_parser.add_argument("name", type=str, help="Name of the agent")
    create_parser.add_argument(
        "--template", 
        choices=["basic", "advanced", "near"], 
        default="basic",
        help="Template to use (basic, advanced, or near)"
    )

    # Run command
    run_parser = subparsers.add_parser("run", help="Run an existing agent")
    run_parser.add_argument("--config", type=str, default="./config.json", help="Path to config.json")
    run_parser.add_argument("--local", action="store_true", help="Run in local mode")
    run_parser.add_argument("--env_path", type=str, default="/tmp/agent_run", help="Environment path")

    # Prepare command
    prepare_parser = subparsers.add_parser("prepare", help="Prepare agent for NEAR AI deployment")
    prepare_parser.add_argument("name", type=str, help="Name of the agent")
    prepare_parser.add_argument("--registry", type=str, help="Custom registry path")

    args = parser.parse_args()

    if args.command == "create":
        create_agent(args.name, args.template)
    elif args.command == "run":
        run_agent(args.config, args.local, args.env_path)
    elif args.command == "prepare":
        prepare_near(args.name, args.registry)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()