import argparse
import os
from near_ai_agent.agent import NearAIAgent

def create_agent(name):
    """
    Create a scaffold for a new agent.
    """
    directory = f"./{name}"
    if not os.path.exists(directory):
        os.makedirs(directory)
        # Create a default configuration file
        with open(f"{directory}/config.json", "w") as config_file:
            config_file.write(
                """{
    "agent_name": "%s",
    "version": "1.0.0",
    "default_tasks": {
        "greet": "Hello! I'm your custom agent.",
        "help": "I can greet and assist with custom tasks."
    }
}""" % name
            )
        # Create a main agent file
        with open(f"{directory}/{name}_agent.py", "w") as agent_file:
            agent_file.write(
                f"""from near_ai_agent.agent import NearAIAgent

class {name.capitalize()}Agent(NearAIAgent):
    pass

if __name__ == "__main__":
    agent = {name.capitalize()}Agent(config_path="./config.json")
    agent.run()
"""
            )
        print(f"Agent '{name}' created successfully in ./{name}/")
    else:
        print(f"Directory '{name}' already exists. Aborting.")

def run_agent(config_path):
    """
    Run an agent using the provided configuration file.
    """
    agent = NearAIAgent(config_path=config_path)
    agent.run()

def main():
    parser = argparse.ArgumentParser(
        description="CLI for managing NEAR AI agents."
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create a new agent scaffold
    create_parser = subparsers.add_parser("create", help="Create a new agent")
    create_parser.add_argument("name", type=str, help="Name of the agent")

    # Run an agent
    run_parser = subparsers.add_parser("run", help="Run an existing agent")
    run_parser.add_argument(
        "--config", type=str, default="./config.json", help="Path to config.json"
    )

    args = parser.parse_args()

    if args.command == "create":
        create_agent(args.name)
    elif args.command == "run":
        run_agent(args.config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
