from typing import Dict, Any, Optional, List
from .base_client import BaseClient

class ChatbotClient(BaseClient):
    """Client for interacting with chatbot endpoints"""

    def create_chatbot(
        self,
        name: str,
        model: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new chatbot instance

        Args:
            name (str): Name of the chatbot
            model (str): Model to use (e.g., 'gpt-4o-mini')
            config (Dict[str, Any]): Configuration including behavior and other settings

        Returns:
            Dict[str, Any]: Created chatbot instance data
        """
        # Convert config to dict if it's a Pydantic model
        if hasattr(config, 'dict'):
            config = config.dict()

        data = {
            'name': name,
            'model': model,
            'config': config
        }

        # Make the API call
        response = self.post('/chatbot/create', data)

        # Ensure all required fields are present
        if not all(key in response for key in ['id', 'name', 'model', 'config', 'user_id', 'created_at', 'is_active']):
            raise ValueError('Invalid response format from server')

        return self.post('/chatbot/create', data)

    def chat(
        self,
        chatbot_id: str,
        message: str,
        image: Optional[str] = None,
        add_to_history: bool = True
    ) -> Dict[str, Any]:
        """Send a message to the chatbot

        Args:
            chatbot_id (str): ID of the chatbot
            message (str): Message to send
            image (Optional[str], optional): Image input - can be URL, base64 string, or file path. Defaults to None.
            add_to_history (bool, optional): Whether to add to chat history. Defaults to True.

        Returns:
            Dict[str, Any]: Chatbot response
        """
        data = {
            'message': message,
            'image': self.process_image(image) if image else None,
            'add_to_history': add_to_history
        }
        return self.post(f'/chatbot/{chatbot_id}/inference', data)

    def get_history(
        self,
        chatbot_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get chat history for a chatbot

        Args:
            chatbot_id (str): ID of the chatbot
            limit (Optional[int], optional): Maximum number of messages to return. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of chat messages
        """
        params = {'limit': limit} if limit else None
        return self.get(f'/chatbot/{chatbot_id}/history', params)

    def delete_chatbot(self, chatbot_id: str) -> Dict[str, Any]:
        """Delete a chatbot instance

        Args:
            chatbot_id (str): ID of the chatbot to delete

        Returns:
            Dict[str, Any]: Deletion confirmation
        """
        return self.delete(f'/chatbot/{chatbot_id}')

    def get_chatbot(self, chatbot_id: str) -> Dict[str, Any]:
        """Get chatbot instance details

        Args:
            chatbot_id (str): ID of the chatbot

        Returns:
            Dict[str, Any]: Chatbot instance data
        """
        return self.get(f'/chatbot/{chatbot_id}')

    def list_chatbots(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all chatbot instances

        Args:
            skip (int, optional): Number of instances to skip. Defaults to 0.
            limit (int, optional): Maximum number of instances to return. Defaults to 100.

        Returns:
            List[Dict[str, Any]]: List of chatbot instances
        """
        params = {
            'skip': skip,
            'limit': limit
        }
        return self.get('/chatbot/list', params)
