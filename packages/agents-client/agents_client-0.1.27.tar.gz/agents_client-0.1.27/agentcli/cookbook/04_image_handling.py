from agentcli.clients import ChatbotClient, AgentClient
import base64
import os
import requests

def main():
    # Initialize clients
    chatbot_client = ChatbotClient()
    agent_client = AgentClient()

    # Example 1: Using local image file
    print("\nExample 1: Using local image file")
    image_path = "cookbook/example_files/test_image.jpg"
    try:
        # Chatbot example
        chatbot_response = chatbot_client.chat(
            chatbot_id="your_chatbot_id",
            message="What's in this image?",
            image=image_path
        )
        print("Chatbot Response:", chatbot_response)

        # Agent example
        agent_response = agent_client.interact(
            agent_id="your_agent_id",
            message="Analyze this image",
            image=image_path
        )
        print("Agent Response:", agent_response)
    except Exception as e:
        print(f"Error processing local image: {e}")

    # Example 2: Using image URL
    print("\nExample 2: Using image URL")
    image_url = "https://example.com/image.jpg"
    try:
        # Chatbot example
        chatbot_response = chatbot_client.chat(
            chatbot_id="your_chatbot_id",
            message="What's in this image?",
            image=image_url
        )
        print("Chatbot Response:", chatbot_response)

        # Agent example
        agent_response = agent_client.interact(
            agent_id="your_agent_id",
            message="Analyze this image",
            image=image_url
        )
        print("Agent Response:", agent_response)
    except Exception as e:
        print(f"Error processing URL image: {e}")

    # Example 3: Using base64 string directly
    print("\nExample 3: Using base64 string")
    try:
        # Create a sample base64 string (in real use, you'd have actual base64 data)
        base64_string = "your_base64_encoded_image_data"
        
        # Chatbot example
        chatbot_response = chatbot_client.chat(
            chatbot_id="your_chatbot_id",
            message="What's in this image?",
            image=base64_string
        )
        print("Chatbot Response:", chatbot_response)

        # Agent example
        agent_response = agent_client.interact(
            agent_id="your_agent_id",
            message="Analyze this image",
            image=base64_string
        )
        print("Agent Response:", agent_response)
    except Exception as e:
        print(f"Error processing base64 image: {e}")

if __name__ == "__main__":
    main()
