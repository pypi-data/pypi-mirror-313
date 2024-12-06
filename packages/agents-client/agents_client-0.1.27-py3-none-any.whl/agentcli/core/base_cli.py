"""Base client implementation for agent interaction."""

import json as json_lib
import time
from typing import Dict, Any, List, Optional, Iterator
import requests
from requests.exceptions import RequestException

from . import command_handler


class AgentClient:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 30):
        """Initialize the API client.

        Args:
            base_url: The base URL of the API server
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.api_key: Optional[str] = None
        self.timeout = timeout
        self.command_executor = command_handler.CommandExecutor()

    def _request(self, method: str, endpoint: str, headers: Optional[Dict[str, str]] = None,
                json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request with proper error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            headers: Request headers
            json_data: JSON payload for POST/PUT requests

        Returns:
            Dict[str, Any]: Response data

        Raises:
            CommandExecutionError: For request or response handling failures
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.request(method, url, headers=headers, json=json_data, timeout=self.timeout)
            
            if response.status_code == 422:
                error_detail = response.json()
                raise command_handler.CommandExecutionError(
                    f"Validation error: {json_lib.dumps(error_detail, indent=2)}\n"
                    f"Request payload: {json_lib.dumps(json_data, indent=2)}"
                )
            
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    raise command_handler.CommandExecutionError(
                        f"Request failed: {str(e)}\n"
                        f"Error details: {json_lib.dumps(error_detail, indent=2)}\n"
                        f"Request payload: {json_lib.dumps(json_data, indent=2)}"
                    ) from e
                except json_lib.JSONDecodeError:
                    pass
            raise command_handler.CommandExecutionError(f"Request failed: {str(e)}") from e
        except json_lib.JSONDecodeError as e:
            raise command_handler.CommandExecutionError(f"Invalid JSON response: {str(e)}") from e

    def interact_stream(self, agent_id: str, message: str,
                       execution_results: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        """Interact with agent using streaming responses.

        Args:
            agent_id: The unique ID of the agent
            message: The message to send to the agent
            execution_results: Optional results from command execution

        Yields:
            Dict[str, Any]: Stream of events from the agent
        """
        if not self.api_key:
            raise command_handler.CommandExecutionError("API key is required")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream"
        }
        payload = {"message": message}

        if execution_results:
            payload["execution_results"] = execution_results

        response = requests.post(
            f"{self.base_url}/api/v1/agent/{agent_id}/interact",
            headers=headers,
            json=payload,
            stream=True,
            timeout=self.timeout
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                try:
                    event = json_lib.loads(line.decode('utf-8').lstrip('data: '))
                    yield event
                except json_lib.JSONDecodeError as e:
                    yield {
                        "type": "error",
                        "data": {"error": f"Failed to parse event: {str(e)}"}
                    }

    def execute_function(self, function_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a function locally and return the result.

        Args:
            function_data: Function execution data from server

        Returns:
            Dict[str, Any]: Function execution result
        """
        try:
            instance_id = function_data.get("instance_id")
            if not instance_id:
                raise ValueError("No instance ID provided")

            command = {
                function_data["function"]: function_data.get("arguments", {})
            }

            result = self.command_executor.execute_command(command, instance_id)
            return {
                "status": "success",
                "sequence_id": function_data.get("sequence_id"),
                "result": result
            }

        except Exception as e:
            return {
                "status": "error",
                "sequence_id": function_data.get("sequence_id"),
                "error": str(e)
            }

    def submit_result(self, agent_id: str, sequence_id: str,
                     result: Dict[str, Any]) -> Dict[str, Any]:
        """Submit function execution result back to the server.

        Args:
            agent_id: The unique ID of the agent
            sequence_id: The sequence ID of the function execution
            result: The execution result

        Returns:
            Dict[str, Any]: Server response
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "sequence_id": sequence_id,
            "result": result
        }

        return self._request(
            "POST",
            f"/api/v1/agent/{agent_id}/function-result",
            headers=headers,
            json_data=payload
        )

    def set_api_key(self, api_key: str) -> None:
        """Set the API key for authentication.

        Args:
            api_key: API key string
        """
        self.api_key = api_key

    def create_agent_with_tools(self, name: str, agent_type: str, behavior: str, tools: Optional[object] = None,
                           config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create agent with tool configuration from class instance.

        Args:
            name: Name of the agent
            agent_type: Type of the agent (e.g., 'chat', 'task')
            behavior: Behavior description for the agent
            tools: Instance of a class with command decorators (optional)
            config: Additional configuration for the agent

        Returns:
            Dict[str, Any]: Agent details

        Raises:
            CommandExecutionError: If agent creation fails
        """
        if not self.api_key:
            raise command_handler.CommandExecutionError("API key is required for this operation")

        # Extract tool configuration if tools provided
        tool_config = {}
        instance_id = None
        if tools:
            tool_config = command_handler.ToolConfigGenerator.extract_command_config(tools)
            instance_id = self.command_executor.register_instance(tools, tool_config)

        # Prepare agent configuration
        agent_config = config or {}
        if instance_id:
            agent_config["instance_id"] = instance_id

        # Create agent
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "name": name,
            "agent_type": agent_type,
            "tool_config": {"tools": tool_config} if tool_config else {},
            "behavior": behavior,
            "config": agent_config
        }

        return self._request("POST", "/api/v1/agent/create", headers=headers, json_data=payload)

    def execute_commands(self, commands: List[Dict[str, Any]], instance_id: str) -> Dict[str, Any]:
        """Execute commands using registered tool instance.

        Args:
            commands: List of commands to execute
            instance_id: ID of the tool instance to use

        Returns:
            Dict[str, Any]: Execution results
        """
        results = {
            "command_results": [],
            "metadata": {
                "start_time": time.time(),
                "command_count": len(commands)
            }
        }

        def execute_single_command(command: Dict[str, Any]) -> Dict[str, Any]:
            try:
                result = self.command_executor.execute_command(command, instance_id)
                return {
                    "command": next(iter(command)),
                    "status": result["status"],
                    "result": result.get("result"),
                    "error": result.get("error"),
                    "execution_time": time.time()
                }
            except Exception as e:
                return {
                    "command": next(iter(command)),
                    "status": "error",
                    "error": str(e),
                    "execution_time": time.time()
                }

        # Execute commands sequentially
        results["command_results"] = [execute_single_command(cmd) for cmd in commands]
        results["metadata"]["end_time"] = time.time()
        results["metadata"]["total_execution_time"] = (
                results["metadata"]["end_time"] - results["metadata"]["start_time"]
        )

        return results

    def process_agent_request(self, agent_id: str, message: str) -> Iterator[Dict[str, Any]]:
        """Process complete agent interaction including command execution with streaming support.

        Args:
            agent_id: ID of the agent to interact with
            message: Message to send to the agent

        Yields:
            Dict[str, Any]: Stream of responses and execution results

        Raises:
            CommandExecutionError: For execution failures
        """
        for event in self.interact_stream(agent_id, message):
            if event.get('type') == 'function_call':
                # Execute function and get result
                instance_id = event.get('context', {}).get('instance_id')
                if not instance_id:
                    raise command_handler.CommandExecutionError("No instance ID provided")

                # Execute command and get result
                execution_result = self.execute_function(event['data'])

                # Submit result back to agent
                self.submit_result(
                    agent_id,
                    event['data'].get('sequence_id'),
                    execution_result
                )

                # Yield execution status
                yield {
                    'type': 'execution_status',
                    'data': execution_result
                }

            else:
                # Pass through other event types (completion, error, etc.)
                yield event

    def interact_with_agent(self, agent_id: int, message: str,
                            execution_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Interact with an agent instance.

        Args:
            agent_id: The unique ID of the agent
            message: The message to send to the agent
            execution_results: Optional results from command execution

        Returns:
            Dict[str, Any]: Response from the agent

        Raises:
            CommandExecutionError: If interaction fails
        """
        if not self.api_key:
            raise command_handler.CommandExecutionError("API key is required for this operation")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"message": message}

        if execution_results:
            payload["execution_results"] = execution_results

        return self._request(
            "POST",
            f"/api/v1/agent/{agent_id}/interact",
            headers=headers,
            json_data=payload
        )
