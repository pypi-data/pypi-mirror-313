"""Command handling module for client-side execution."""

import uuid
import logging
import traceback
import inspect

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('command_handler_debug.log'),
                              logging.StreamHandler()])
logger = logging.getLogger('CommandHandler')

class CommandExecutionError(Exception):
    """Raised when a command execution fails"""

class ToolConfigGenerator:
    @staticmethod
    def _command_to_dict(cmd) -> dict:
        """Convert a Command object to a dictionary format.

        Args:
            cmd: Command object from decorator

        Returns:
            dict: JSON-serializable command configuration
        """
        return {
            'name': cmd.name,
            'description': cmd.description,
            'parameters': cmd.parameters
        }

    @staticmethod
    def extract_command_config(instance: object) -> dict:
        """Extract command configurations from a class instance.

        Args:
            instance: Object instance containing command-decorated methods

        Returns:
            dict: Tool configuration in the format expected by the agent
        """
        tool_config = {}
        
        for attr_name in dir(instance):
            attr = getattr(instance, attr_name)
            if hasattr(attr, 'command'):
                section = getattr(attr, 'section', 'Default')
                if section not in tool_config:
                    tool_config[section] = {}
                
                # Convert command to dictionary format
                cmd = attr.command
                cmd_dict = ToolConfigGenerator._command_to_dict(cmd)
                tool_config[section][cmd.name] = cmd_dict
                # Convert parameters to dictionary with parameter names as keys
                param_dict = {}
                for param in cmd.parameters:
                    param_data = param.__dict__()
                    param_name = param_data.pop('name')
                    param_dict[param_name] = param_data
                cmd_dict['parameters'] = param_dict

                print(f'Command Dict: {cmd_dict}')

        return tool_config


class CommandExecutor:
    def __init__(self):
        self.instances = {}
        self.configs = {}
    
    def register_instance(self, instance: object, config: dict) -> str:
        """Register an instance for command execution.

        Args:
            instance: Object instance containing the commands
            config: Tool configuration for the instance

        Returns:
            str: Instance ID for future reference
        """
        instance_id = str(uuid.uuid4())
        self.instances[instance_id] = instance
        self.configs[instance_id] = config
        return instance_id
    
    def execute_command(self, command: dict, instance_id: str) -> dict:
        """Execute a command using the registered instance.

        Args:
            command: Command dictionary with name and parameters
            instance_id: ID of the instance to use

        Returns:
            dict: Execution result
        """
        if instance_id not in self.instances:
            return {
                'status': 'error',
                'error': 'Instance not found'
            }

        instance = self.instances[instance_id]

        try:
            logger.debug('\n=== Command Execution Details ===')
            logger.debug(f'Command Dict: {command}')
            logger.debug(f'Instance ID: {instance_id}')
            logger.debug(f'Instance Type: {type(instance)}')
            logger.debug(f'Instance Attributes: {dir(instance)}')
            logger.debug(f'Instance Dict: {vars(instance)}')

            # Get command name and args
            cmd_name = next(iter(command))
            cmd_args = command[cmd_name]
            logger.debug(f'Command Name: {cmd_name}')
            logger.debug(f'Command Args: {cmd_args}')

            # Find method with matching command name
            logger.debug('\n=== Searching for Command Method ===')
            for attr_name in dir(instance):
                attr = getattr(instance, attr_name)
                logger.debug(f'Checking attribute: {attr_name}')
                logger.debug(f'Attribute type: {type(attr)}')
                logger.debug(f'Has command attribute: {hasattr(attr, "command")}')
                
                if hasattr(attr, 'command') and attr.command.name == cmd_name:
                    logger.debug(f'Found matching command: {cmd_name}')
                    logger.debug(f'Command object: {attr.command}')
                    logger.debug('Executing command...')
                    result = attr(**cmd_args)
                    logger.debug(f'Execution result: {result}')
                    return {
                        'status': 'success',
                        'result': result
                    }

            return {
                'status': 'error',
                'error': f'Command {cmd_name} not found'
            }

        except (AttributeError, TypeError, ValueError, KeyError) as e:
            logger.error('\n=== Command Execution Error ===')
            logger.error(f'Error Type: {type(e).__name__}')
            logger.error(f'Error Message: {str(e)}')
            logger.error(f'Error Location: {traceback.extract_tb(e.__traceback__)[-1]}')
            logger.error('\nFull Stack Trace:')
            logger.error(traceback.format_exc())
            
            # Log object state at time of error
            logger.error('\nObject State at Error:')
            if hasattr(instance, '__dict__'):
                logger.error(f'Instance Variables: {vars(instance)}')
            
            # Log specific attribute access that failed
            if isinstance(e, AttributeError):
                missing_attr = str(e).split("'")[1] if "'" in str(e) else 'unknown'
                logger.error(f'\nMissing Attribute: {missing_attr}')
                logger.error(f'Available Attributes: {dir(instance)}')
            
            return {
                'status': 'error',
                'error': f'Command execution failed: {str(e)}',
                'error_type': type(e).__name__,
                'error_location': str(traceback.extract_tb(e.__traceback__)[-1])
            }