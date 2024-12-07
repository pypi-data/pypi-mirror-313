import asyncio
import pytest
from promptstudio_sdk import PromptStudio
from datetime import datetime

# Test configuration with real API key
TEST_CONFIG = {
    "api_key": "yLSjOm26OZCqFjMDXGBrZOKIC98qpYMv",  # Real API key
    "env": "test",
    "bypass": True,  # Enable bypass mode for direct AI platform calls
}


@pytest.fixture
def client():
    return PromptStudio(TEST_CONFIG)


@pytest.mark.asyncio
async def test_summarized_memory_with_image():
    """Test summarized memory with image input"""
    client = PromptStudio(TEST_CONFIG)

    # Test data with real prompt ID and image
    interaction_request = {
        "user_message": [
            {
                "type": "text",
                "text": "Hello, I have a patient Narpat, check his face for symptoms",
            },
            {
                "type": "file",
                "file_url": {
                    "url": "https://regionalneurological.com/wp-content/uploads/2019/08/AdobeStock_244803452.jpeg"
                },
            },
        ],
        "memory_type": "summarizedMemory",
        "session_id": "",  # New session
        "env": "test",
        "request_from": "test",
    }

    # Execute the function with real prompt ID
    response = await client.summarizedmemory_save_log_ai_interaction_prompt(
        user_prompt_id="66f660e33e6e774719e30e93",
        interaction_request=interaction_request,
    )

    # Assertions
    assert response is not None
    assert "message" in response
    assert "user_prompt_id" in response
    assert "response" in response
    assert "session_id" in response
    print("Response:", response)


@pytest.mark.asyncio
async def test_summarized_memory_follow_up():
    """Test summarized memory with follow-up question in same session"""
    client = PromptStudio(TEST_CONFIG)

    # First interaction to establish session
    first_interaction = {
        "user_message": [
            {
                "type": "text",
                "text": "Hello, I have a patient Narpat, check his face for symptoms",
            },
            {
                "type": "file",
                "file_url": {
                    "url": "https://regionalneurological.com/wp-content/uploads/2019/08/AdobeStock_244803452.jpeg"
                },
            },
        ],
        "memory_type": "summarizedMemory",
        "session_id": "",
        "env": "test",
        "request_from": "test",
    }

    first_response = await client.summarizedmemory_save_log_ai_interaction_prompt(
        user_prompt_id="66f660e33e6e774719e30e93", interaction_request=first_interaction
    )

    # Follow-up interaction using same session
    follow_up_interaction = {
        "user_message": [
            {"type": "text", "text": "What other symptoms should I look for?"}
        ],
        "memory_type": "summarizedMemory",
        "session_id": first_response["session_id"],  # Use session from first response
        "env": "test",
        "request_from": "test",
    }

    follow_up_response = await client.summarizedmemory_save_log_ai_interaction_prompt(
        user_prompt_id="66f660e33e6e774719e30e93",
        interaction_request=follow_up_interaction,
    )

    # Assertions
    assert follow_up_response is not None
    assert follow_up_response["session_id"] == first_response["session_id"]
    assert "response" in follow_up_response
    print("Follow-up Response:", follow_up_response)


@pytest.mark.asyncio
async def test_summarized_memory_with_variables():
    """Test summarized memory with variables"""
    client = PromptStudio(TEST_CONFIG)

    interaction_request = {
        "user_message": [
            {
                "type": "text",
                "text": "Hello, I have a patient {{patient_name}}, check his face for symptoms",
            },
            {
                "type": "file",
                "file_url": {
                    "url": "https://regionalneurological.com/wp-content/uploads/2019/08/AdobeStock_244803452.jpeg"
                },
            },
        ],
        "memory_type": "summarizedMemory",
        "session_id": "",
        "env": "test",
        "request_from": "test",
        "variables": {"patient_name": "John Smith"},
    }

    response = await client.summarizedmemory_save_log_ai_interaction_prompt(
        user_prompt_id="66f660e33e6e774719e30e93",
        interaction_request=interaction_request,
    )

    # Assertions
    assert response is not None
    assert "message" in response
    assert "response" in response
    print("Response with variables:", response)


if __name__ == "__main__":
    pytest.main(["-v", "test_summarized_memory.py"])
