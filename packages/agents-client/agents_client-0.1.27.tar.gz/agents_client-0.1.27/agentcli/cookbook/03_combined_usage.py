#!/usr/bin/env python3
"""Combined Usage Example

This example demonstrates how to use both ChatbotClient and AgentClient
in a single application. It shows:
1. Creating and configuring both types of instances
2. Basic interactions with both
3. Error handling
4. State management
"""
import traceback

from agentcli.clients import AgentClient, ChatbotClient
from agentcli.clients.base_client import ApiError, AuthenticationError

def main():
    # Initialize both clients
    base_url = "http://localhost:8000"
    chatbot_client = ChatbotClient(base_url)
    agent_client = AgentClient(base_url)

    # Set API key for both clients
    api_key = "your-api-key"
    chatbot_client.set_api_key(api_key)
    agent_client.set_api_key(api_key)

    try:
        # Create a chatbot instance
        chatbot_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        chatbot = chatbot_client.create_chatbot(
            name="AssistantBot",
            model="gpt-4o-mini",
            behavior="A helpful assistant that provides clear and concise answers.",
            config=chatbot_config
        )
        print(f"Created chatbot: {chatbot['id']}\n")

        # Create an agent instance
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

        agent = agent_client.create_agent(
            name="ResearchAgent",
            agent_type="research",
            behavior="A research agent that helps find and analyze information.",
            tools=agent_tools,
            config=agent_config
        )
        print(f"Created agent: {agent['id']}\n")

        # Demonstrate chatbot interaction
        print("=== Chatbot Interaction ===")
        chat_response = chatbot_client.chat(
            chatbot['id'],
            "What's the weather like today?"
        )
        print(f"Chatbot response: {chat_response['data']['response']}\n")

        # Demonstrate agent interaction
        print("=== Agent Interaction ===")
        agent_response = agent_client.interact(
            agent['id'],
            "Find information about Python programming."
        )
        print(f"Agent response: {agent_response['data']['response']}\n")

        # Demonstrate error handling
        print("=== Error Handling ===")
        try:
            # Try to interact with non-existent chatbot
            chatbot_client.chat("invalid-id", "Hello!")
        except ApiError as e:
            print(f"Handled API error: {str(e)}\n")

        # Get chatbot history
        print("=== Chatbot History ===")
        history = chatbot_client.get_history(chatbot['id'])
        print(f"Chat history: {history}\n")

        # Get agent state
        print("=== Agent State ===")
        state = agent_client.get_state(agent['id'])
        print(f"Agent state: {state}\n")

    except AuthenticationError as e:
        print(f"Authentication error: {str(e)}")
    except ApiError as e:
        print(f"API error: {str(traceback.format_exc())}")
    except Exception as e:
        print(f"Unexpected error: {str(traceback.format_exc())}")

if __name__ == "__main__":
    main()
