# NEAR AI Agent (WIP)

A Python package and command-line interface (CLI) for building and managing AI agents on NEAR Protocol. This package helps developers quickly scaffold, customize, and run their own agents using the NEAR AI Environment API.

## Features

- Full integration with NEAR AI's Environment API for context and state management.
- CLI for creating and managing agents.
- Modular design for extending with custom tasks and logic.
- Configurable via `config.json`.

---

## Installation

Install the package from PyPI:
```bash
pip install near_ai_agent
```

Alternatively, install locally for development:
```bash
pip install -e .
```

---

## Usage

### **Using as a Python Module**

#### Create and Run a Custom Agent
You can subclass the `NearAIAgent` class to define your own tasks and behavior.

```python
from near_ai_agent.agent import NearAIAgent
from near_ai_agent.tasks import calculate_sum

class CustomAgent(NearAIAgent):
    def handle_task(self, task, *args):
        if task == "calculate_sum":
            return self.environment.output(calculate_sum(*args))
        return super().handle_task(task, *args)

if __name__ == "__main__":
    agent = CustomAgent()
    agent.run()
```

#### Run a Preconfigured Agent
Use the default `NearAIAgent` with a `config.json` file:
```python
from near_ai_agent.agent import NearAIAgent

agent = NearAIAgent(config_path="./config.json")
agent.run()
```

#### Example: Task Execution
```python
from near_ai_agent.agent import NearAIAgent

agent = NearAIAgent(config_path="./config.json")

# Handle a default task
response = agent.handle_task("greet")
print(response)

# Handle a custom task
response = agent.handle_task("calculate_sum", "10", "20")
print(response)
```

---

### **Using the Command-Line Interface (CLI)**

#### Create a New Agent
To scaffold a new agent with a default configuration:
```bash
near-ai-agent create my_agent
```

This will create a directory `./my_agent/` with the following structure:
```
my_agent/
├── config.json
└── my_agent_agent.py
```

#### Run an Existing Agent
To run an agent with a specific configuration file:
```bash
near-ai-agent run --config ./my_agent/config.json
```

#### Available Commands
```bash
near-ai-agent --help
```
Output:
```
usage: near-ai-agent [-h] {create,run} ...

CLI for managing NEAR AI agents.

positional arguments:
  {create,run}          Commands
    create              Create a new agent
    run                 Run an existing agent

optional arguments:
  -h, --help            Show this help message and exit
```

---

## Configuration

The agent behavior is controlled by the `config.json` file. Below is an example configuration:

```json
{
    "agent_name": "MyCustomAgent",
    "version": "1.0.0",
    "default_tasks": {
        "greet": "Hello! I'm MyCustomAgent, here to assist you.",
        "help": "I can greet and help you with basic tasks."
    }
}
```

You can define custom tasks in the `default_tasks` section and extend the agent's functionality in Python.

---

## Extending the Package

#### Add a Custom Task
1. Define a new task in `tasks.py`:
   ```python
   def calculate_sum(*numbers):
       return f"The sum is: {sum(map(int, numbers))}"
   ```

2. Update `handle_task` in your custom agent:
   ```python
   class CustomAgent(NearAIAgent):
       def handle_task(self, task, *args):
           if task == "calculate_sum":
               return self.environment.output(calculate_sum(*args))
           return super().handle_task(task, *args)
   ```

3. Test the task:
   ```bash
   near-ai-agent run --config ./my_agent/config.json
   ```

#### Integrate with Real APIs
Replace the placeholders in `tasks.py` with calls to real APIs or databases:
```python
import requests

def provide_weather(location):
    api_key = "your_api_key"
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}")
    data = response.json()
    return f"The weather in {location} is {data['current']['condition']['text']} with a temperature of {data['current']['temp_c']}°C."
```

---

## Testing

Run tests using `unittest`:
```bash
python -m unittest discover tests
```

---

## Example Workflow

1. Install the package:
   ```bash
   pip install near_ai_agent
   ```

2. Create a new agent:
   ```bash
   near-ai-agent create my_agent
   ```

3. Add custom tasks or modify `config.json`.

4. Run the agent:
   ```bash
   near-ai-agent run --config ./my_agent/config.json
   ```

5. Extend the agent as needed by editing the scaffolded files.

---

## License

This project is licensed under the MIT License.

---