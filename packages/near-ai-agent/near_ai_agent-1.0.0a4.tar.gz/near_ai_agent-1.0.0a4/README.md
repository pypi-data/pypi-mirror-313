# NEAR AI Agent (WIP)

A Python package and command-line interface (CLI) for building and managing AI agents on NEAR Protocol. This package helps developers quickly scaffold, customize, and run their own agents using the NEAR AI Environment API, with support for both local development and NEAR AI deployment.

## Features

- Full integration with NEAR AI's Environment API for context and state management
- Enhanced CLI for creating, running, and deploying agents
- Support for both local development and NEAR AI deployment
- Built-in tool registry for extending agent capabilities
- Multiple agent templates for different use cases
- Configurable via `config.json` and `metadata.json`
- Modular design for custom task integration

## Installation

Install the package from PyPI:
```bash
pip install near_ai_agent
```

For development:
```bash
git clone https://github.com/joe-rlo/near_ai_agent
cd near_ai_agent
pip install -e .
```

## Command-Line Interface (CLI)

The package provides a comprehensive CLI for managing agents:

### Create a New Agent
```bash
# Create with basic template
near-ai-agent create my-agent

# Create with NEAR AI deployment template
near-ai-agent create my-agent --template near

# Create with advanced features
near-ai-agent create my-agent --template advanced
```

This creates a directory with the following structure:
```
my-agent/
├── config.json                 # Agent configuration
├── my-agent_agent.py          # Main agent implementation
├── run.py                     # Example usage script
└── metadata.json              # (Only with --template near)
```

### Run an Agent
```bash
# Run locally with mock environment
near-ai-agent run --config ./my-agent/config.json --local

# Run with custom environment path
near-ai-agent run --config ./my-agent/config.json --env_path /custom/path
```

### Prepare for NEAR AI Deployment
```bash
# Prepare agent for deployment
near-ai-agent prepare my-agent

# Prepare with custom registry path
near-ai-agent prepare my-agent --registry /custom/registry/path
```

## Using as a Python Module

### Basic Usage
```python
from near_ai_agent.agent import NearAIAgent

# For local development
from near_ai_agent.environment import NearAIEnvironment
env = NearAIEnvironment()  # Creates mock environment
agent = NearAIAgent(env=env)
agent.run()

# For NEAR AI deployment
agent = NearAIAgent()  # Environment provided by NEAR AI
agent.run()
```

### Custom Agent with Tools
```python
from near_ai_agent.agent import NearAIAgent

class CustomAgent(NearAIAgent):
    def _register_tools(self):
        super()._register_tools()  # Register default tools
        
        @self.tool_registry.register_tool
        def calculate_sum(a: int, b: int) -> int:
            """Calculate the sum of two numbers"""
            return a + b

# Initialize and run
agent = CustomAgent()
agent.run()
```

## Configuration

### Local Configuration (config.json)
```json
{
    "agent_name": "MyCustomAgent",
    "version": "1.0.0",
    "system_prompt": {
        "role": "system",
        "content": "You are a helpful AI assistant."
    },
    "model": "qwen2p5-72b-instruct",
    "temperature": 0.7,
    "default_tasks": {
        "greet": "Hello! I'm your custom agent.",
        "help": "I can help with various tasks."
    }
}
```

### NEAR AI Deployment (metadata.json)
```json
{
    "category": "agent",
    "description": "Your agent description",
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
    "show_entry": true,
    "name": "my-custom-agent",
    "version": "0.1.0"
}
```

## Development Workflow

1. Create a new agent:
```bash
near-ai-agent create my-agent --template near
```

2. Develop and test locally:
```bash
near-ai-agent run --config ./my-agent/config.json --local
```

3. Prepare for NEAR AI deployment:
```bash
near-ai-agent prepare my-agent
```

4. Deploy to NEAR AI:
```bash
nearai registry upload ~/.nearai/registry/my-agent
```

5. Run on NEAR AI:
```bash
nearai agent interactive my-agent --local
```

## Testing

Run tests using unittest:
```bash
python -m unittest discover tests
```

## Example Templates

The CLI provides three templates for different use cases:

### Basic Template
- Simple agent with default tasks
- Good for getting started and basic use cases

### Advanced Template
- Includes tool registry support
- Custom task implementation
- Enhanced message processing

### NEAR Template
- Full NEAR AI deployment setup
- Model configuration
- Metadata for registry
- Tool integration

## License

This project is licensed under the MIT License.

---

For more detailed information about building agents on NEAR AI, please visit the [NEAR AI documentation](https://docs.near.ai/).