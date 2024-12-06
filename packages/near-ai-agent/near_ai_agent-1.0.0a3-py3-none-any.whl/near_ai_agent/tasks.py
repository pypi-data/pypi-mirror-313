def main():
    """Example of how to use the agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run the NEAR AI agent")
    parser.add_argument("--local", action="store_true", help="Run in local mode")
    parser.add_argument("--execution_folder", default="/tmp/agent_run", 
                       help="Folder for agent execution")
    
    args = parser.parse_args()
    
    if args.local:
        # Local development mode
        from near_ai_agent.mock_env import MockEnvironment
        env = MockEnvironment(args.execution_folder)
    else:
        # Production mode - env will be provided by NEAR AI
        raise ValueError("This script is for local testing only")
    
    agent = NearAIAgent(env)
    agent.run()
    
def fetch_user_info(user_id):
    """
    Retrieve user information.
    Replace this with a real database or API call.
    """
    return {"user_id": user_id, "name": "John Doe", "role": "developer"}

def provide_weather(location):
    """
    Provide weather information.
    Replace this with a real weather API call.
    """
    return f"The weather in {location} is sunny with a temperature of 25°C."

if __name__ == "__main__":
    main()