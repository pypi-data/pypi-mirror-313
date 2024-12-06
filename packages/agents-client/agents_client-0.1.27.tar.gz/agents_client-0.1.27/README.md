# Agents Client Library

## Overview
The Agents Client Library provides a simple interface for interacting with the Agents API. It handles authentication, request management, and provides convenient methods for managing chatbots and agentcli.

## Installation

### From PyPI
```bash
pip install agents-client
```

## Configuration
The client library uses a `config.json` file for API settings. You can either use the default configuration or provide your own:

```python
from agentcli.client import AgentClient

# Using default configuration
client = AgentClient()

# Using custom configuration file
client = AgentClient(config_path='path/to/config.json')

# Override configuration programmatically
client = AgentClient(base_url='https://api.example.com', api_version='v2')
```

### Configuration Options
- `base_url`: API base URL
- `version`: API version
- `timeout`: Request timeout in seconds
- `retry_attempts`: Number of retry attempts
- `retry_delay`: Delay between retries in seconds

See `config.json` for all available options.

## Quick Start

### Basic Usage
```python
from agentcli import ChatbotClient
from agentcli.base_client import ApiError, AuthenticationError

# Initialize client
base_url = "http://localhost:8000"
chatbot = ChatbotClient(base_url)

# Set API key
api_key = "your-api-key"
chatbot.set_api_key(api_key)

try:
    # Create a chatbot instance
    config = {
        "temperature": 0.7,
        "max_tokens": 4000,
        "behavior": "A helpful assistant that provides clear and concise answers."
    }

    # Create the chatbot
    response = chatbot.create_chatbot(
        name="BasicChat",
        model="gpt-4o-mini",
        config=config
    )

    # Store chatbot ID
    chatbot_id = response.get('id')
    print(f"Created chatbot with ID: {chatbot_id}\n")

    # Example conversation
    message = "Hello! How are you?"
    chat_response = chatbot.chat(chatbot_id, message)
    print(f"Chatbot: {chat_response.get('response', 'No response')}\n")

except AuthenticationError as e:
    print(f"Authentication error: {str(e)}")
except ApiError as e:
    print(f"API error: {str(e)}")
```

### Async Streaming Example
```python
from agentcli.client import AgentClient
import asyncio

async def main():
    # Initialize client with async context manager
    async with AgentClient("http://localhost:8000") as client:
        client.set_api_key("your-api-key")

        # Create an agent with API execution mode
        config = {
            "behavior": "task-focused",
            "model": "gpt-4o-mini",
            "api_mode": True  # Enable API execution mode
        }
        agent = await client.create_agent_with_tools(
            name="FileManager",
            model="gpt-4o-mini",
            tools=FileTools(),  # Your tool class instance
            config=config
        )

        # Stream interactions with the agent
        async for event in client.process_agent_request(agent["id"], "Update debug mode in config.json"):
            if event["type"] == "function_call":
                print(f"Executing function: {event['data']['function']}")
                # Function is automatically executed by the client
            elif event["type"] == "execution_status":
                print(f"Execution result: {event['data']}")
            elif event["type"] == "completion":
                print(f"Task completed: {event['data']}")
            elif event["type"] == "error":
                print(f"Error: {event['data']}")

# Run the async client
asyncio.run(main())
```

### State Management Example
```python
async with AgentClient("http://localhost:8000") as client:
    # State is automatically synchronized
    async for event in client.process_agent_request(agent_id, message):
        if event["type"] == "state_update":
            print(f"Agent state updated: {event['data']}")
        elif event["type"] == "function_call":
            # State is preserved across function calls
            result = await client.execute_function(event["data"])
            # State is automatically updated with function results
            await client.submit_result(agent_id, event["data"]["sequence_id"], result)
```

## Chatbot Operations

### Creating a Chatbot
```python
from agentcli import ChatbotClient
from agentcli.base_client import ApiError, AuthenticationError

# Initialize client
base_url = "http://localhost:8000"
chatbot_client = ChatbotClient(base_url)

# Set API key
api_key = "your-api-key"
chatbot_client.set_api_key(api_key)

try:
    # Define configuration
    config = {
        "temperature": 0.7,
        "max_tokens": 4000,
        "behavior": "A helpful assistant that provides clear and concise answers."
    }

    # Create the chatbot
    response = chatbot_client.create_chatbot(
        name="BasicChat",
        model="gpt-4o-mini",
        config=config
    )

    # Store chatbot ID
    chatbot_id = response.get('id')
    print(f"Created chatbot with ID: {chatbot_id}\n")

except AuthenticationError as e:
    print(f"Authentication error: {str(e)}")
except ApiError as e:
    print(f"API error: {str(e)}")
```

### Listing Chatbots
```python
chatbots = client.list_chatbots()
for bot in chatbots:
    print(f"Bot: {bot['name']} (ID: {bot['id']})")
```

### Chatbot Interaction
```python
try:
    # Example conversation
    print("=== Chatbot Interaction ===\n")
    chat_response = chatbot_client.chat(
        chatbot_id,
        "What's the weather like today?"
    )
    print(f"Chatbot: {chat_response['data']['response']}\n")

    # Get chatbot history
    print("=== Chatbot History ===\n")
    history = chatbot_client.get_history(chatbot_id)
    print(f"Chat history: {history}\n")

except ApiError as e:
    print(f"API Error: {str(e)}\n")
```

### Updating Chatbots
```python
updated_config = {
    "temperature": 0.8,
    "max_tokens": 1000
}

updated_bot = client.update_chatbot(
    chatbot_id=123,
    name="UpdatedBot",
    model="gpt-4o-mini",
    config=updated_config
)
```

### Deleting Chatbots
```python
result = client.delete_chatbot(chatbot_id=123)
```

## Image Handling

Both ChatbotClient and AgentClient support simplified image handling. You can use images in three ways:

```python
# Using a URL
chatbot.chat(
    chatbot_id='id',
    message='What's in this image?',
    image='https://example.com/image.jpg'
)

# Using a local file path
chatbot.chat(
    chatbot_id='id',
    message='What's in this image?',
    image='path/to/local/image.jpg'
)

# Using base64 string directly
chatbot.chat(
    chatbot_id='id',
    message='What's in this image?',
    image=base64_string
)
```

The system automatically detects the type of input and handles it appropriately. The same functionality is available for AgentClient:

```python
agent.interact(
    agent_id='id',
    message='Analyze this image',
    image='path/to/image.jpg'  # Can be URL, file path, or base64
)
```

## Agent Operations

### Creating an Agent
```python
from agentcli import AgentClient
from agentcli.base_client import ApiError, AuthenticationError

# Initialize client
base_url = "http://localhost:8000"
agent_client = AgentClient(base_url)

# Set API key
api_key = "your-api-key"
agent_client.set_api_key(api_key)

try:
    # Define agent tools and configuration
    agent_tools = {
        "general": {
            "search": {
                "name": "search",
                "description": "Search for information",
                "parameters": {}
            }
        }
    }

    agent_config = {
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 4000
    }

    # Create the agent
    agent = agent_client.create_agent(
        name="ResearchAgent",
        agent_type="research",
        behavior="A research agent that helps find and analyze information.",
        tools=agent_tools,
        config=agent_config
    )
    print(f"Created agent with ID: {agent['id']}\n")

except AuthenticationError as e:
    print(f"Authentication error: {str(e)}")
except ApiError as e:
    print(f"API error: {str(e)}")
```

### Listing Agents
```python
agents = client.list_agents()
for agent in agents:
    print(f"Agent: {agent['name']} (ID: {agent['id']})")
```

### Agent Interaction
```python
try:
    # Demonstrate agent interaction
    print("=== Agent Interaction ===\n")
    agent_response = agent_client.interact(
        agent['id'],
        "Find information about Python programming."
    )
    print(f"Agent response: {agent_response['data']['response']}\n")

    # Get agent state
    print("=== Agent State ===\n")
    state = agent_client.get_state(agent['id'])
    print(f"Agent state: {state}\n")

    # Demonstrate error handling
    print("=== Error Handling ===\n")
    try:
        # Try to interact with non-existent agent
        agent_client.interact("invalid-id", "Hello!")
    except ApiError as e:
        print(f"Handled API error: {str(e)}\n")

except AuthenticationError as e:
    print(f"Authentication error: {str(e)}")
except ApiError as e:
    print(f"API error: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

The new system simplifies command execution by:
```

Key features of the new command system:
- Automatic command execution and result handling
- Built-in command validation and safety checks
- Simplified tool registration using decorators
- Automatic result mapping in responses
- Support for both synchronous and asynchronous operations
- Comprehensive error handling and reporting

### Supported Commands
The client can execute various commands locally:

```python
# File operations
commands = [
    {"view_file": {"file_path": "config.json"}},
    {"smart_replace": {
        "file_path": "config.json",
        "old_text": "debug: false",
        "new_text": "debug: true"
    }},
    {"create_file": {
        "file_path": "new_file.txt",
        "content": "Hello, world!"
    }}
]

# Execute commands with safety checks
results = client.execute_commands(commands, context={})
```

### Command Execution Safety
- File path validation
- Comprehensive error handling
- Safe text replacement
- Automatic retries for network issues

```python
# Example with error handling
try:
    results = client.execute_commands(commands, context={})
    if any(r["status"] == "error" for r in results["command_results"]):
        print("Some commands failed to execute")
        for result in results["command_results"]:
            if result["status"] == "error":
                print(f"Error: {result['error']}")
except Exception as e:
    print(f"Execution failed: {str(e)}")
```

## Streaming Operations

### Basic Streaming
```python
async with AgentClient("http://localhost:8000") as client:
    # Stream responses from agent
    async for event in client.interact_stream(agent_id, message):
        if event["type"] == "function_call":
            # Handle function execution
            result = await client.execute_function(event["data"])
            await client.submit_result(agent_id, event["data"]["sequence_id"], result)
        elif event["type"] == "completion":
            print(f"Completed: {event['data']}")
```

### Concurrent Command Execution
```python
async def process_commands(client, commands, instance_id):
    # Commands are executed concurrently
    results = await client.execute_commands(commands, instance_id)
    return results
```

## Error Handling
The client includes comprehensive error handling with streaming support:

### Streaming Error Handling
```python
async with AgentClient("http://localhost:8000") as client:
    try:
        async for event in client.interact_stream(agent_id, message):
            if event["type"] == "error":
                print(f"Error occurred: {event['data']}")
                break
            elif event["type"] == "function_call":
                try:
                    result = await client.execute_function(event["data"])
                    await client.submit_result(
                        agent_id,
                        event["data"]["sequence_id"],
                        result
                    )
                except Exception as e:
                    print(f"Function execution error: {e}")
    except Exception as e:
        print(f"Stream error: {e}")
```

### Command Execution Errors
```python
try:
    results = client.execute_commands(commands, context)
    for result in results['command_results']:
        if result['status'] == 'error':
            print(f"Command {result['command']} failed: {result['error']}")
except client.CommandExecutionError as e:
    print(f"Execution error: {str(e)}")
```

### API Errors
```python
try:
    chatbot = client.get_chatbot(999)
except Exception as e:
    print(f"API error: {str(e)}")
```

## Best Practices
1. Always handle API errors in production code
2. Store API keys securely
3. Use appropriate timeouts for API calls
4. Monitor rate limits
5. Implement proper error handling
6. Validate file paths before operations
7. Use context information for better error tracking
8. Implement proper retry strategies

### Error Handling Best Practices
```python
# Comprehensive error handling example
try:
    # Initial interaction
    response = client.interact_with_agent(agent_id, message)
    
    if response['status'] == 'pending_execution':
        try:
            # Execute commands with safety checks
            results = client.execute_commands(
                response['commands'],
                response.get('context', {})
            )
            
            # Check individual command results
            failed_commands = [
                r for r in results['command_results']
                if r['status'] == 'error'
            ]
            
            if failed_commands:
                print("Some commands failed:")
                for cmd in failed_commands:
                    print(f"- {cmd['command']}: {cmd['error']}")
            
            # Continue interaction with results
            final_response = client.interact_with_agent(
                agent_id,
                message,
                execution_results=results
            )
            
        except client.CommandExecutionError as e:
            print(f"Command execution failed: {e}")
            # Handle command execution failure
            
except Exception as e:
    print(f"Interaction failed: {e}")
    # Handle interaction failure
```

## Advanced Usage

### Custom Headers
```python
client = AgentClient(
    base_url="http://localhost:8000",
    headers={"Custom-Header": "value"}
)
```

### Batch Operations
```python
# Create multiple chatbots
configs = [
    {"name": "Bot1", "model": "gpt-4o-mini", "config": {...}},
    {"name": "Bot2", "model": "gpt-4o-mini", "config": {...}}
]

chatbots = []
for config in configs:
    bot = client.create_chatbot(**config)
    chatbots.append(bot)
```