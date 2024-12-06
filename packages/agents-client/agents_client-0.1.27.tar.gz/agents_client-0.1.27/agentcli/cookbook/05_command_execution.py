"""Example of using the AgentClient with automatic command execution."""

from agentcli.clients import AgentClient
from agentcli.core.command_handler import ToolConfigGenerator

class CommandTools:
    def view_file(self, file_path: str) -> str:
        """View contents of a file"""
        with open(file_path, 'r') as f:
            return f.read()

    def search_project(self, search_term: str) -> list:
        """Search for a term in project files"""
        return [f"Found in file{i}.txt" for i in range(1, 3)]  # Example results

async def main():
    # Initialize client and tools
    client = AgentClient()
    tools = CommandTools()
    
    # Generate tool config
    tool_config = ToolConfigGenerator.extract_command_config(tools)
    
    # Register tools with the interpreter
    client.interpreter.register_command_instance(tools, tool_config)
    
    # Create an agent with the tools
    agent = client.create_agent(
        name="File Helper",
        agent_type="file_operations",
        behavior="I help with file operations",
        tools=tool_config
    )
    
    # Example interaction that will trigger command execution
    response = await client.interact(
        agent_id=agent['id'],
        message="What's in the README.md file?"
    )
    
    print("Agent Response:", response)
    
    # The client automatically:
    # 1. Receives commands from the agent
    # 2. Executes them using the registered tools
    # 3. Sends results back to the agent
    # 4. Gets the final response

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
