#!/usr/bin/env python3
"""Basic Chat Example

This example demonstrates simple chat interaction with the chatbot service.
It shows how to:
1. Initialize the client
2. Create a chatbot instance with proper configuration
3. Send messages and receive responses
4. Handle errors
"""

import json

from agentcli.schemas.chatbot import ChatbotConfig
from agentcli.clients import ChatbotClient
from agentcli.clients import ApiError, AuthenticationError


def debug_print_response(response):
    """Print response data for debugging"""
    print("\nDebug: Raw Response Data:")
    print(json.dumps(response, indent=2, default=str))
    print("\nAvailable fields:", list(response.keys()))


def create_chatbot_instance(chatbot_client: ChatbotClient, name: str, model: str, config: dict) -> dict:
    """Create a chatbot instance and return raw response for debugging"""
    # First create the ChatbotConfig object
    config_obj = ChatbotConfig(**config)
    
    # Create the chatbot and get raw response
    response = chatbot_client.create_chatbot(
        name=name,
        model=model,
        config=config_obj.dict()
    )
    
    # Print debug info
    debug_print_response(response)
    return response


def main():
    # Initialize client
    base_url = "http://0.0.0.0:8000"
    chatbot = ChatbotClient(base_url)

    # Set API key
    api_key = "ICW_AQdBh7hkx98CwMSB9cOIAwpY9OkDFcQHMtdAp4E"
    chatbot.set_api_key(api_key)

    try:
        # Create a chatbot instance
        print("=== Creating Chatbot ===\n")
        
        # Define configuration
        config = {
            "temperature": 0.7,
            "max_tokens": 4000,
            "behavior": "A helpful assistant that provides clear and concise answers.",
        }

        try:
            # Get raw response first for debugging
            response = create_chatbot_instance(
                chatbot_client=chatbot,
                name="BasicChat",
                model="gpt-4o-mini",
                config=config
            )

            # Store chatbot ID for further use
            chatbot_id = response.get('id')
            if not chatbot_id:
                raise ValueError("No chatbot ID in response")

            print(f"Created chatbot with ID: {chatbot_id}\n")

            # Example conversation
            print("=== Chatbot Conversation ===\n")
            messages = [
                "Hello! How are you?",
                "What did I just say?",
                "Thank you!"
            ]

            for message in messages:
                print(f"User: {message}")
                try:
                    chat_response = chatbot.chat(chatbot_id, message)
                    print(f"Chatbot: {chat_response.get('response', 'No response')}\n")
                except ApiError as e:
                    print(f"API Error: {str(e)}\n")

        except ValueError as e:
            print(f"Validation error: {str(e)}")

    except AuthenticationError as e:
        print(f"Authentication error: {str(e)}")
    except ApiError as e:
        print(f"API error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
