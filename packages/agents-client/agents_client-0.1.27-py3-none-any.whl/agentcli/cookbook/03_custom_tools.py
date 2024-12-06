#!/usr/bin/env python3
"""Custom Tools Example

This example demonstrates how to create and use custom tools with the agent service.
It shows how to:
1. Define custom tools
2. Configure an agent with custom tools
3. Use the tools in interactions
4. Handle tool-related errors
"""

from agentcli.clients import AgentClient
from agentcli.clients.base_client import ApiError, AuthenticationError

def main():
    # Initialize client
    base_url = "http://localhost:8000"
    agent = AgentClient(base_url)

    # Set API key
    api_key = "your-api-key"
    agent.set_api_key(api_key)

    try:
        # Define custom tools
        custom_tools = {
            "math_ops": {
                "calculator": {
                    "name": "calculator",
                    "description": "Perform basic mathematical calculations",
                    "parameters": {
                        "expression": "str"
                    }
                },
                "unit_converter": {
                    "name": "unit_converter",
                    "description": "Convert between different units",
                    "parameters": {
                        "value": "float",
                        "from_unit": "str",
                        "to_unit": "str"
                    }
                }
            },
            "text_ops": {
                "text_analyzer": {
                    "name": "text_analyzer",
                    "description": "Analyze text for statistics",
                    "parameters": {
                        "text": "str"
                    }
                }
            }
        }

        # Create agent with custom tools
        print("=== Creating Agent with Custom Tools ===\n")
        agent_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 4000
        }

        agent_instance = agent.create_agent(
            name="CustomToolsAgent",
            agent_type="utility",
            behavior="An agent that helps with calculations and text analysis.",
            tools=custom_tools,
            config=agent_config
        )
        print(f"Created agent: {agent_instance['id']}\n")

        # Example tool usage
        print("=== Using Custom Tools ===\n")

        # Calculator example
        print("User: Can you calculate 15 * 7 + 22?")
        response = agent.interact(
            agent_instance['id'],
            "Calculate 15 * 7 + 22"
        )
        print(f"Agent: {response['response']}\n")

        # Unit converter example
        print("User: Convert 5 kilometers to miles")
        response = agent.interact(
            agent_instance['id'],
            "Convert 5 kilometers to miles"
        )
        print(f"Agent: {response['response']}\n")

        # Text analyzer example
        print("User: Analyze this text: 'The quick brown fox jumps over the lazy dog.'")
        response = agent.interact(
            agent_instance['id'],
            "Analyze this text: 'The quick brown fox jumps over the lazy dog.'"
        )
        print(f"Agent: {response['response']}\n")

        # Error handling example
        print("=== Error Handling ===\n")
        try:
            # Try invalid calculation
            response = agent.interact(
                agent_instance['id'],
                "Calculate 1/0"
            )
        except ApiError as e:
            print(f"Expected error handled: {str(e)}\n")

        # Combined tools example
        print("=== Combined Tools Usage ===\n")
        print("User: Calculate 25 * 4 and analyze the result as text")
        response = agent.interact(
            agent_instance['id'],
            "First calculate 25 * 4, then analyze that number as text"
        )
        print(f"Agent: {response['response']}\n")

    except AuthenticationError as e:
        print(f"Authentication error: {str(e)}")
    except ApiError as e:
        print(f"API error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
