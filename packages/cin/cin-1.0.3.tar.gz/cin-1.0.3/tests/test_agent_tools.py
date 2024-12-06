# Standard libraries
import unittest
import sys
from unittest.mock import patch

# Internal library
sys.path.append('src')
from cin.agent import Agent


# Define multiple sample functions
def sample_function_one(a: int, b: int) -> int:
    """
    Adds two integers and returns the result.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b

def sample_function_two(name: str, age: int = 30) -> str:
    """
    Generates a greeting message.

    Args:
        name (str): The name of the person.
        age (int, optional): The age of the person. Defaults to 30.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! You are {age} years old."

def empty_function():
    pass



class TestAgent(unittest.TestCase):
    def test_tool_functions_works_correctly(self):
        # Arrange
        agent: Agent = Agent(
            name="Test Agent",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
            tools=[sample_function_one, sample_function_two]
        )

        expected_tool_information = '{\n    "name": "sample_function_one",\n    "description": "Adds two integers and returns the result.\\n\\nArgs:\\n    a (int): The first integer.\\n    b (int): The second integer.\\n\\nReturns:\\n    int: The sum of a and b."\n}\n\n{\n    "name": "sample_function_two",\n    "description": "Generates a greeting message.\\n\\nArgs:\\n    name (str): The name of the person.\\n    age (int, optional): The age of the person. Defaults to 30.\\n\\nReturns:\\n    str: A greeting message."\n}\n\n{\n    "name": "execution_completed",\n    "description": "Returns a message indicating that there are no other tools or agents to call as we have the information we need.\\n\\nParameters:\\n    None\\n\\nReturns:\\n    str: A message indicating that the execution has been completed."\n}'

        tool_information = agent.get_tool_information()
        self.assertEqual(tool_information, expected_tool_information)

    def test_tool_functions_throws_error_when_docstring_of_function_is_empty(self):
        # Arrange
        agent: Agent = Agent(
            name="Test Agent",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
            tools=[empty_function]
        )

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            agent.get_tool_information()

        self.assertEqual(
            str(context.exception),
            "Function 'empty_function' does not have a docstring."
        )

    def test_tool_functions_is_none_when_tool_list_is_empty(self):
        # Arrange
        agent: Agent = Agent(
            name="Test Agent",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
            tools=[]
        )

        # Act & Assert
        tool_information = agent.get_tool_information()

        self.assertIsNone(None)






