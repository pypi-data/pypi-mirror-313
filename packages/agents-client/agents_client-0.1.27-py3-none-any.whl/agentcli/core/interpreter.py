"""Client-side command interpreter for executing agent commands and collecting results."""

import logging
import traceback
import time
from typing import Dict, Any, Optional
from .command_handler import CommandExecutor, CommandExecutionError

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('interpreter_debug.log'),
                              logging.StreamHandler()])
logger = logging.getLogger('ClientInterpreter')

class ClientInterpreter:
    """Interprets and executes commands from agent responses."""

    def __init__(self):
        self.command_executor = CommandExecutor()
        self.current_results: Dict[str, Any] = {}
        self._registered_instance_id: Optional[str] = None
        self.logger = logging.getLogger('ClientInterpreter')

    def register_command_instance(self, instance: object, config: dict) -> None:
        """Register a command instance for execution.

        Args:
            instance: Object instance containing the commands
            config: Tool configuration for the instance
        """
        self._registered_instance_id = self.command_executor.register_instance(instance, config)

    def execute_command(self, cmd_name: str, cmd_args: dict) -> Any:
        """Execute a single command and return its result.

        Args:
            cmd_name: Name of the command to execute
            cmd_args: Arguments for the command

        Returns:
            Any: Result of the command execution

        Raises:
            CommandExecutionError: If command execution fails
        """
        logger.debug(f'\n=== Command Execution Start ===\n')
        logger.debug(f'Command Name: {cmd_name}')
        logger.debug(f'Command Args: {cmd_args}')
        logger.debug(f'Instance ID: {self._registered_instance_id}')
        logger.debug(f'Executor State: {vars(self.command_executor)}')
        if not self._registered_instance_id:
            raise CommandExecutionError("No command instance registered")

        command = {cmd_name: cmd_args}
        result = self.command_executor.execute_command(command, self._registered_instance_id)

        if result['status'] == 'error':
            raise CommandExecutionError(result['error'])

        return result['result']

    def interpret_response(self, agent_response: dict) -> Optional[Dict[str, Any]]:
        """Interpret an agent response and execute any actions.

        Args:
            agent_response: Response from the agent containing actions to execute

        Returns:
            Optional[Dict[str, Any]]: Command results if feedback is needed, None otherwise

        Raises:
            CommandExecutionError: If command execution fails
        """
        self.current_results = {}
        
        # Get actions from the response
        actions = []
        if 'context' in agent_response and 'agent_response' in agent_response['context']:
            response_obj = agent_response['context']['agent_response']
            if isinstance(response_obj, dict) and 'response' in response_obj:
                actions = response_obj['response'].get('actions', [])
        
        self.logger.debug(f'Processing actions: {actions}')
        needs_feedback = False
        results = {}

        for action in actions:
            # Each action is a dict with one key (action name) and value (args)
            action_name = list(action.keys())[0]
            action_args = action[action_name]
            
            try:
                logger.debug(f'\n=== Before Action Execution ===\n')
                logger.debug(f'Action: {action_name}')
                logger.debug(f'Arguments: {action_args}')
                
                if action_name == 'feedback':
                    needs_feedback = True
                    continue
                
                result = self.execute_command(action_name, action_args)
                results[action_name] = {
                    'status': 'success',
                    'result': result
                }
                self.current_results[action_name] = result
                
                logger.debug(f'\n=== After Action Execution ===\n')
                logger.debug(f'Result: {result}')
                
            except CommandExecutionError as e:
                logger.error(f'Action execution error: {str(e)}')
                self.current_results[action_name] = {
                    'status': 'error',
                    'error': str(e)
                }
            except Exception as e:
                logger.error(f'Unexpected error in action {action_name}: {str(e)}')
                self.current_results[action_name] = {
                    'status': 'error',
                    'error': f'Unexpected error: {str(e)}'
                }

        # Handle feedback and final response
        if needs_feedback:
            request_id = ''
            if 'agent_response' in agent_response.get('context', {}):
                request_id = agent_response['context']['agent_response'].get('request_id', str(time.time()))
            else:
                request_id = str(time.time())
            
            # Format results as list of command/result pairs for server
            formatted_results = [
                {
                    'command': cmd_name,
                    'result': cmd_result['result'] if isinstance(cmd_result, dict) and 'result' in cmd_result else cmd_result
                }
                for cmd_name, cmd_result in self.current_results.items()
            ]
            
            feedback_response = {
                'command_results': formatted_results,
                'request_id': request_id
            }
            
            logger.debug(f'\n=== Sending Feedback ===\n')
            logger.debug(f'Feedback Response: {feedback_response}')
            
            return feedback_response
        
        return None

    def get_current_results(self) -> Dict[str, Any]:
        """Get the results of the most recent command executions.

        Returns:
            Dict[str, Any]: Dictionary of command results
        """
        return self.current_results

    def clear_results(self) -> None:
        """Clear the current results."""
        self.current_results = {}
