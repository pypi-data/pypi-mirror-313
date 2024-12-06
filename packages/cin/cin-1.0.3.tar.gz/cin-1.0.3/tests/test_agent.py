# Standard libraries
import unittest
import sys

# Library dependencies
sys.path.append('src')
from cin.agent import Agent


class TestAgent(unittest.TestCase):
    def test_unsupported_model_with_supported_endpoint(self):
        # Arrange and Act
        with self.assertRaises(ValueError) as context:
            agent: Agent = Agent(
                name="Test Agent",
                description="A test agent",
                endpoint="openai-v1-chat-completions",
                model="unsupported-model",
                temperature=0.7,
                top_p=0.9,
                instructions="You are a helpful assistant.",
                metadata={"source": "test"}
            )

        # Assert err message is contained in the exception
        exception = context.exception
        self.assertIsInstance(exception, ValueError)
        self.assertIn(
            "An endpoint 'openai-v1-chat-completions' and model name 'unsupported-model' is not supported. Please check the endpoint and model name.",
            str(exception)
        )

    def test_unsupported_endpoint_with_supported_model(self):
        # Arrange and Act
        with self.assertRaises(ValueError) as context:
            agent: Agent = Agent(
                name="Test Agent",
                description="A test agent",
                endpoint="unsupported-endpoint",
                model="gpt-4o-2024-08-06",
                temperature=0.7,
                top_p=0.9,
                instructions="You are a helpful assistant.",
                metadata={"source": "test"}
            )

        # Assert err message is contained in the exception
        exception = context.exception
        self.assertIsInstance(exception, ValueError)
        self.assertIn(
            "An endpoint 'unsupported-endpoint' and model name 'gpt-4o-2024-08-06' is not supported. Please check the endpoint and model name.",
            str(exception)
        )

    def test_unsupported_endpoint_and_unsupported_model(self):
        # Arrange and Act
        with self.assertRaises(ValueError) as context:
            agent: Agent = Agent(
                name="Test Agent",
                description="A test agent",
                endpoint="unsupported-endpoint",
                model="unsupported-model",
                temperature=0.7,
                top_p=0.9,
                instructions="You are a helpful assistant.",
                metadata={"source": "test"}
            )

        # Assert err message is contained in the exception
        exception = context.exception
        self.assertIsInstance(exception, ValueError)
        self.assertIn(
            "An endpoint 'unsupported-endpoint' and model name 'unsupported-model' is not supported. Please check the endpoint and model name.",
            str(exception)
        )

    def test_validation_validate_endpoint_api_keys(self):
        # Test missing API key for OpenAI endpoint
        with self.assertRaises(ValueError) as context_openai:
            agent_openai: Agent = Agent(
                name="Test Agent OpenAI",
                description="A test agent for OpenAI",
                endpoint="openai-v1-chat-completions",
                model="gpt-4o-2024-08-06",
                temperature=0.7,
                top_p=0.9,
                instructions="You are a helpful assistant.",
                metadata={"source": "test"},
            )

        exception_openai = context_openai.exception
        self.assertIsInstance(exception_openai, ValueError)
        self.assertIn(
            "OPENAI_API_KEY environment variable is not set.",
            str(exception_openai)
        )

        # Test missing API key for Anthropic endpoint
        with self.assertRaises(ValueError) as context_anthropic:
            agent_anthropic: Agent = Agent(
                name="Test Agent Anthropic",
                description="A test agent for Anthropic",
                endpoint="anthropic-v1-messages",
                model="claude-3-5-sonnet-20241022",
                temperature=0.7,
                top_p=0.9,
                instructions="You are a helpful assistant.",
                metadata={"source": "test"},
            )

        exception_anthropic = context_anthropic.exception
        self.assertIsInstance(exception_anthropic, ValueError)
        self.assertIn(
            "ANTHROPIC_API_KEY environment variable is not set.",
            str(exception_anthropic)
        )
