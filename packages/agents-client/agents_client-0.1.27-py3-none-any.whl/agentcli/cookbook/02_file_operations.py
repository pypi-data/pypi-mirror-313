#!/usr/bin/env python3
"""File Operations Example with Recursive Feedback Pattern

This example demonstrates how to work with files using the agent service,
showing the recursive feedback pattern where commands and their results
are processed in a continuous loop until the agent sends a complete action.

Key concepts demonstrated:
1. Initialize the agent client and tools
2. Register command instances with the interpreter
3. Handle the recursive feedback pattern:
   - Agent sends commands
   - Commands are executed
   - Results are sent back via feedback
   - Loop continues until complete action
4. Error handling within the feedback loop

The feedback loop works like this:
1. Agent receives a user message
2. Agent sends one or more commands
3. Each command is executed
4. Results are sent back via feedback
5. Agent processes feedback and may send more commands
6. Loop continues until agent sends complete
7. Final response is returned to user
"""
import traceback
import sys
from agentcli.clients import AgentClient
from agentcli.clients.base_client import ApiError, AuthenticationError
from agentcli.core.command_handler import ToolConfigGenerator
from agentcli.core.decorators import command
class FileTools:
    @command(
        name='read_file',
        description='Reads content from a file at the specified path',
        parameters={
            'file_path': {
                'type': 'str',
                'description': 'Path to the file to read',
                'required': True
            }
        }
    )
    def read_file(self, file_path: str) -> str:
        """Read content from a file"""
        with open(file_path, 'r') as f:
            return f.read()

    @command(
        name='write_file',
        description='Writes content to a file at the specified path',
        parameters={
            'file_path': {
                'type': 'str',
                'description': 'Path to the file to write',
                'required': True
            },
            'content': {
                'type': 'str',
                'description': 'Content to write to the file',
                'required': True
            }
        }
    )
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file"""
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"

def main():
    # Initialize clients
    base_url = "http://localhost:8000"
    agent = AgentClient()

    # Set API key
    api_key = "your-api-key"
    agent.set_api_key(api_key)

    try:
        # Create an agent with file handling tools
        print("=== Creating File Processing Agent ===\n")
        tools = FileTools()
        file_tools = ToolConfigGenerator.extract_command_config(tools)
        print(f"Extracted tools: {file_tools}\n")
        
        # Register tools with the interpreter
        agent.interpreter.register_command_instance(tools, file_tools)

        agent_config = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "max_tokens": 4000
        }

        agent_instance = agent.create_agent(
            name="FileAgent",
            agent_type="file_processor",
            behavior="An agent that helps with file operations and content processing.\nHere are your tools: {tools}",
            tools=file_tools,
            config=agent_config
        )
        print(f"Created agent: {agent_instance['id']}\n")

        # Example file operations
        print("=== File Operations ===\n")

        # Create a test file
        test_content = "Hello, this is a test file.\nIt contains multiple lines.\nPlease process this content."
        test_file = "example_files/test.txt"

        # Example 1: Simple file creation with feedback loop
        print("\n=== Example 1: File Creation with Feedback ===\n")
        print("User: Please create a test file with some content.")
        response = agent.interact(
            agent_instance['id'],
            f"Create a file at {test_file} with this content: {test_content}"
        )
        # The interact method will automatically handle the feedback loop:
        # 1. Agent sends write_file command
        # 2. Command is executed, results sent back via feedback
        # 3. Agent processes feedback and sends complete
        print("Response after feedback loop completed:")
        print(response)
        # Example 2: Multi-step operation with feedback
        print("\n=== Example 2: Read and Modify with Multiple Feedbacks ===\n")
        print("User: Please read the file, summarize it, and add a timestamp.")
        response = agent.interact(
            agent_instance['id'],
            f"Read {test_file}, give me a summary, and then add the current time to the end of the file."
        )
        # This will demonstrate multiple feedback cycles:
        # 1. Agent sends read_file command
        # 2. Gets content via feedback
        # 3. Processes content and sends write_file command
        # 4. Gets write confirmation via feedback
        # 5. Finally sends complete with summary
        print("Response after multiple feedback cycles:")
        print(response)

        # Example 3: Error handling in feedback loop
        print("\n=== Example 3: Error Handling in Feedback Loop ===\n")
        print("User: Please process a non-existent file.")
        try:
            response = agent.interact(
                agent_instance['id'],
                "Read the file missing.txt and append 'test' to it"
            )
            # The feedback loop will properly handle the error:
            # 1. Agent sends read_file command
            # 2. Gets error via feedback
            # 3. Agent handles error and sends complete
            print("Response after error handling:")
            print(response)
        except ApiError as e:
            print(f"Error properly handled: {str(e)}\n")

        # Error handling example
        print("=== Error Handling ===\n")
        try:
            # Try to read non-existent file
            response = agent.interact(
                agent_instance['id'],
                "Read the file at non_existent.txt"
            )
        except ApiError as e:
            print(f"Expected error handled: {str(e)}\n")

    except AuthenticationError as e:
        print(f"Authentication error: {str(traceback.format_exc())}")
    except ApiError as e:
        print(f"API error: {str(traceback.format_exc())}")
    except Exception as e:
        print(f"Unexpected error: {str(traceback.format_exc())}")

if __name__ == "__main__":
    main()
