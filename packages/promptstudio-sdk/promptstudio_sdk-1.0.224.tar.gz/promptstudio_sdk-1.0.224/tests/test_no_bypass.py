import os
from promptstudio_sdk import PromptStudio
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from promptstudio_sdk.cache import InteractionCacheManager, CacheManager
import pytest
import logging

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create logger for this test file
logger = logging.getLogger(__name__)


# Add this decorator to capture logs
@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO)


# Load environment variables
load_dotenv()


@pytest.mark.asyncio
async def test_chat_with_prompt_no_bypass():
    # Initialize PromptStudio with bypass=False
    client = PromptStudio(
        {
            "api_key": "nDBabew4CGIKD8uKnOqOajG8AZgczzgW",
            "env": "test",
            "bypass": False,  # Set bypass to False
        }
    )

    try:
        # Before interaction
        print("\nCache contents before interaction:")

        # Use a clean prompt ID
        prompt_id = "671f7ea3895439853685b020"
        session_id = "test_session_123"
        version = 1  # Version as integer for chat_with_prompt

        # Make the chat request using chat_with_prompt
        response = await client.chat_with_prompt(
            prompt_id=prompt_id,
            user_message=[{"type": "text", "text": "What's the weather like today?"}],
            memory_type="fullMemory",
            window_size=10,
            session_id=session_id,
            variables={},
            version=version,  # Optional version parameter
        )
        print(f"response ID: {session_id}")

        print("Test Execution Successful!")
        print("\nResponse Content:")
        print(response)
        print("\nExecution Details:")
        print(f"Session ID: {session_id}")
        print(f"Environment: test")
        print(f"Bypass Mode: False")

        # Verify response structure from PromptStudio API
        assert isinstance(response, dict), "Response should be a dictionary"
        assert "data" in response, "Response should contain 'data' key"
        assert "message" in response, "Response should contain 'message' key"

        # Verify nested response structure
        data = response.get("data", {})
        assert "response" in data, "Response data should contain 'response' key"
        assert "session_id" in data, "Response data should contain 'session_id' key"
        assert (
            "user_prompt_id" in data
        ), "Response data should contain 'user_prompt_id' key"
        assert "message" in data, "Response data should contain 'message' key"

        # Verify response content
        assert isinstance(data["response"], str), "Response content should be a string"
        assert data["session_id"] == session_id, "Session ID should match"

    except Exception as e:
        print(f"Error during execution: {str(e)}")
        raise


def test_your_test_function(caplog):
    # Your test code here

    # Assert that the specific log message was captured
    assert "Your specific log message" in caplog.text


if __name__ == "__main__":
    asyncio.run(test_chat_with_prompt_no_bypass())
