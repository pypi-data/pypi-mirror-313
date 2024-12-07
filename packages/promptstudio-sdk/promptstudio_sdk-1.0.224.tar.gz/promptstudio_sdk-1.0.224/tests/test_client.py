import pytest
from promptstudio_sdk.client import PromptStudio


def test_client_initialization():
    # Test initialization with test environment
    client = PromptStudio({"api_key": "test_key", "env": "test"})
    assert client.api_key == "test_key"
    assert client.env == "test"
    assert client.bypass == False
    assert client.base_url == "https://api.playground.promptstudio.dev/api/v1"

    # Test initialization with bypass
    client = PromptStudio({"api_key": "test_key", "env": "test", "bypass": True})
    assert client.bypass == True


def test_client_inheritance():
    # Test that the client inherits all methods from PromptManager
    client = PromptStudio({"api_key": "test_key", "env": "test"})

    # Check that the client has the required methods
    assert hasattr(client, "get_all_prompts")
    assert hasattr(client, "chat_with_prompt")
    assert callable(client.get_all_prompts)
    assert callable(client.chat_with_prompt)


@pytest.mark.asyncio
async def test_client_integration():
    client = PromptStudio({"api_key": "test_key", "env": "test"})

    # Mock the _request method
    async def mock_request(endpoint, method="GET", **kwargs):
        if endpoint == "/test_folder":
            return {"data": {"versions": []}}
        elif endpoint == "/chat_with_prompt_version/test_prompt":
            return {"response": "Hello there!"}
        return {}

    # Replace _request with our mock
    client._request = mock_request

    # Test get_all_prompts
    prompts_response = await client.get_all_prompts("test_folder")
    assert prompts_response == {"data": {"versions": []}}

    # Test chat_with_prompt - now with await
    chat_response = await client.chat_with_prompt(
        prompt_id="test_prompt",
        user_message=[{"type": "text", "text": "Hello"}],
        memory_type="fullMemory",
        window_size=10,
        session_id="test_session",
        variables={},
    )
    assert chat_response == {"response": "Hello there!"}
