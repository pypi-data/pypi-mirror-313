# Standard libraries
import unittest
import sys
from unittest.mock import patch

# Internal library
sys.path.append('src')
from cin.agent import Agent

class TestAgent(unittest.TestCase):
    def test_get_available_agents_works_correctly(self):
        agent1: Agent = Agent(
            name="Test Agent 1",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
            tools=[]
        )

        agent2: Agent = Agent(
            name="Test Agent 2",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
            interaction=[agent1],
            tools=[]
        )

        expected = '{\n    "name": "Test Agent 1",\n    "description": "A test agent Parameters: request (str): The information you are requesting from this agent. The request should start with I am requesting.. \\n Returns: response"\n}'

        available_agents = agent2.get_available_agents()
        self.assertEqual(available_agents, expected)

    def test_get_available_agents_returns_none_when_empty(self):
        agent1: Agent = Agent(
            name="Test Agent 1",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
        )

        agent2: Agent = Agent(
            name="Test Agent 2",
            description="A test agent",
            endpoint="openai-v1-chat-completions",
            model="gpt-4o-2024-08-06",
            api_key="test-api-key",
        )

        available_agents = agent2.get_available_agents()
        self.assertIsNone(available_agents)








