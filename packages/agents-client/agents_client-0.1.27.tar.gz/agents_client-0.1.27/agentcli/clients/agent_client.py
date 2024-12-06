import json
import logging
from typing import Dict, Any, Optional, List
from .base_client import BaseClient, ApiError, AuthenticationError
from agentcli.core.interpreter import ClientInterpreter

logger = logging.getLogger(__name__)

class AgentClient(BaseClient):
    """Client for interacting with agent endpoints"""

    def __init__(self):
        super().__init__()
        self.interpreter = ClientInterpreter()

    def create_agent(
        self,
        name: str,
        agent_type: str,
        behavior: str,
        tools: Dict[str, Any],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new agent instance

        Args:
            name (str): Name of the agent
            agent_type (str): Type of agent (e.g., 'general', 'coding', etc.)
            behavior (str): Behavior description
            tools (Dict[str, Any]): Tool configuration
            config (Optional[Dict[str, Any]], optional): Additional configuration. Defaults to None.

        Returns:
            Dict[str, Any]: Created agent instance data
        """
        data = {
            'name': name,
            'agent_type': agent_type,
            'behavior': behavior,
            'tool_config': tools,
            'config': config or {}
        }
        return self.post('/agent/create', data)

    def _process_response(self, response) -> Dict[str, Any]:
        """Process JSON response from agent interaction

        Args:
            response: Response object from requests

        Returns:
            Dict[str, Any]: Processed response data
        """
        try:
            logger.debug('\n=== Processing Response ===')
            logger.debug(f'Response Status: {response.status_code}')
            logger.debug(f'Response Headers: {dict(response.headers)}')
            
            response_data = response.json()
            logger.debug(f'Parsed Response Data: {response_data}')
            
            # Add metadata if available
            if 'metadata' in response_data:
                metadata = response_data['metadata']
                logger.debug(f'Processing Metadata: {metadata}')
                if 'model' in metadata:
                    metadata['model_name'] = metadata['model']
                    logger.debug('Added model_name to metadata')
            
            # Log command execution data if present
            if 'commands_to_execute' in response_data:
                logger.debug(f'Found commands to execute: {response_data["commands_to_execute"]}')
                    
            return response_data
            
        except json.JSONDecodeError as e:
            raise ApiError(f'Failed to parse response: {str(e)}\nResponse text: {response.text}')

    def interact(
        self,
        agent_id: str,
        message: str,
        image: Optional[str] = None,
        command_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a message to the agent and handle any command execution

        Args:
            agent_id (str): ID of the agent
            message (str): Message to send
            image (Optional[str], optional): Image input - can be URL, base64 string, or file path. Defaults to None.
            command_results (Optional[Dict[str, Any]], optional): Results from previous commands. Defaults to None.

        Returns:
            Dict[str, Any]: Agent response
        """
        if not self.api_key:
            raise AuthenticationError('API key not set. Call set_api_key() first.')

        data = {
            'message': message,
            'image': self.process_image(image) if image else None,
            'command_results': command_results
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        response = self.session.post(
            url=f'{self.base_url}/api/{self.api_version}/agent/{agent_id}/interact',
            json=data,
            headers=headers
        )

        if response.status_code != 200:
            raise ApiError(f'Request failed with status {response.status_code}: {response.text}')

        # Process response
        response_data = self._process_response(response)

        # Extract actions from response
        actions = []
        if 'context' in response_data and 'agent_response' in response_data['context']:
            response_obj = response_data['context']['agent_response']
            if isinstance(response_obj, dict) and 'response' in response_obj:
                actions = response_obj['response'].get('actions', [])

        # Process actions if present
        if actions:
            logger.debug(f'Found actions to process: {actions}')
            # Check for complete action
            if any(action.get('complete', {}) for action in actions):
                logger.debug('Found complete action - ending feedback chain')
                return response_data

            # Execute commands and continue feedback chain
            results = self.interpreter.interpret_response(response_data)
            if results:
                logger.debug(f'Got command results: {results}')
                # Send results back and continue interaction
                return self.interact(agent_id, message, command_results=results)

        return response_data

    def get_state(
        self,
        agent_id: str
    ) -> Dict[str, Any]:
        """Get current state of an agent

        Args:
            agent_id (str): ID of the agent

        Returns:
            Dict[str, Any]: Agent state data
        """
        return self.get(f'/agent/{agent_id}/state')

    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """Delete an agent instance

        Args:
            agent_id (str): ID of the agent to delete

        Returns:
            Dict[str, Any]: Deletion confirmation
        """
        return self.delete(f'/agent/{agent_id}')

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """Get agent instance details

        Args:
            agent_id (str): ID of the agent

        Returns:
            Dict[str, Any]: Agent instance data
        """
        return self.get(f'/agent/{agent_id}')

    def list_agents(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all agent instances

        Args:
            skip (int, optional): Number of instances to skip. Defaults to 0.
            limit (int, optional): Maximum number of instances to return. Defaults to 100.

        Returns:
            List[Dict[str, Any]]: List of agent instances
        """
        params = {
            'skip': skip,
            'limit': limit
        }
        return self.get('/agent/list', params)

    def update_agent(
        self,
        agent_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update agent configuration

        Args:
            agent_id (str): ID of the agent
            updates (Dict[str, Any]): Updated fields

        Returns:
            Dict[str, Any]: Updated agent instance data
        """
        return self.post(f'/agent/{agent_id}/update', updates)
