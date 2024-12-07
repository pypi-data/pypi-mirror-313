import pytest
from unittest.mock import Mock, patch, AsyncMock
import json
import logging
from datetime import datetime
from promptstudio_sdk.prompt import PromptManager
from bson import ObjectId

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,  # This will override any existing logging configuration
)
logger = logging.getLogger(__name__)


# Configure logging for tests
@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level(logging.INFO)
    # Ensure root logger also shows INFO
    logging.getLogger().setLevel(logging.INFO)
    yield


@pytest.fixture
def prompt_manager():
    logger.info("Creating PromptManager instance for testing")
    return PromptManager(config={"api_key": "test_key", "env": "test"})


@pytest.fixture
def mock_interaction_request():
    logger.info("Creating mock interaction request")
    request = {
        "user_message": [{"type": "text", "text": "Hello, how are you?"}],
        "memory_type": "summarizedMemory",
        "window_size": 10,
        "session_id": "",
        "env": "test",
        "request_from": "sdk",
        "variables": {},
        "version": 1,
    }
    logger.info(f"Mock interaction request created: {request}")
    return request


@pytest.fixture
def mock_user_prompt():
    logger.info("Creating mock user prompt")
    prompt = {
        "platform": "openai",
        "aiPlatform": {"platform": "openai", "model": "gpt-3.5-turbo"},
    }
    logger.info(f"Mock user prompt created: {prompt}")
    return prompt


@pytest.fixture
def mock_prompt_details():
    logger.info("Creating mock prompt details")
    details = {
        "ai_platform": "openai",
        "model": "gpt-3.5-turbo",
        "system_prompt": "You are a helpful assistant",
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.9,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "response_format": {"type": "text"},
        "version": 1,
        "variables": [
            {"name": "var1", "value": "default1"},
            {"name": "var2", "value": "default2"},
        ],
    }
    logger.info(f"Mock prompt details created: {details}")
    return details


@pytest.mark.asyncio
async def test_summarymemory_new_session(
    prompt_manager, mock_interaction_request, mock_user_prompt, mock_prompt_details
):
    logger.info("\n" + "=" * 50)
    logger.info("Starting test_summarymemory_new_session")
    logger.info("=" * 50)

    # Mock the necessary methods
    logger.info("Setting up mock methods")
    prompt_manager._fetch_and_cache_prompt_details = AsyncMock(
        return_value=mock_prompt_details
    )

    mock_ai_response = {
        "response": "This is the AI response",
        "content": [{"type": "text", "text": "This is the AI response"}],
    }
    logger.info(f"Mock AI response prepared: {mock_ai_response}")

    prompt_manager._make_ai_platform_request = AsyncMock(return_value=mock_ai_response)

    # Mock cache managers
    logger.info("Mocking cache managers")
    with patch("promptstudio_sdk.prompt.CacheManager") as mock_cache_manager, patch(
        "promptstudio_sdk.prompt.InteractionCacheManager"
    ) as mock_interaction_cache:

        mock_cache_manager.get_prompt_details.return_value = None
        mock_interaction_cache.get_interaction_history.return_value = None

        logger.info("Executing summarymemory_save_log_ai_interaction_prompt")
        try:
            result = await prompt_manager.summarymemory_save_log_ai_interaction_prompt(
                user_id="test_user",
                user_prompt_id="test_prompt",
                user_prompt=mock_user_prompt,
                interaction_request=mock_interaction_request,
            )

            logger.info(f"Result received: {result}")

            # Assertions
            logger.info("Performing assertions")
            assert (
                result["message"]
                == "AI interaction saved successfully for memory type: summarized memory"
            )
            assert "session_id" in result
            assert "response" in result
            assert result["user_prompt_id"] == "test_prompt"

            logger.info("All assertions passed successfully")

        except Exception as e:
            logger.error(f"Test failed with error: {str(e)}")
            raise

    logger.info("Test completed successfully")


@pytest.mark.asyncio
async def test_summarymemory_existing_session(
    prompt_manager, mock_interaction_request, mock_user_prompt, mock_prompt_details
):
    logger.info("\n" + "=" * 50)
    logger.info("Starting test_summarymemory_existing_session")
    logger.info("=" * 50)

    # Modify mock_interaction_request for existing session
    mock_interaction_request["session_id"] = str(ObjectId())
    logger.info(f"Using session_id: {mock_interaction_request['session_id']}")

    # Mock existing interaction history
    logger.info("Creating mock interaction history")
    existing_history = {
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": "Previous message"}]},
            {
                "role": "assistant",
                "content": [{"type": "text", "text": "Previous response"}],
            },
        ],
        "memory_type": "summarizedMemory",
        "summarized_content": "Previous conversation summary",
    }
    logger.info(f"Mock interaction history created: {existing_history}")

    # Mock the necessary methods
    logger.info("Setting up mock methods")
    prompt_manager._fetch_and_cache_prompt_details = AsyncMock(
        return_value=mock_prompt_details
    )

    mock_ai_response = {
        "response": "This is the AI response",
        "content": [{"type": "text", "text": "This is the AI response"}],
    }
    logger.info(f"Mock AI response prepared: {mock_ai_response}")

    prompt_manager._make_ai_platform_request = AsyncMock(return_value=mock_ai_response)

    # Mock cache managers
    logger.info("Mocking cache managers")
    with patch("promptstudio_sdk.prompt.CacheManager") as mock_cache_manager, patch(
        "promptstudio_sdk.prompt.InteractionCacheManager"
    ) as mock_interaction_cache:

        mock_cache_manager.get_prompt_details.return_value = None
        mock_interaction_cache.get_interaction_history.return_value = existing_history

        logger.info("Executing summarymemory_save_log_ai_interaction_prompt")
        try:
            result = await prompt_manager.summarymemory_save_log_ai_interaction_prompt(
                user_id="test_user",
                user_prompt_id="test_prompt",
                user_prompt=mock_user_prompt,
                interaction_request=mock_interaction_request,
            )

            logger.info(f"Result received: {result}")

            # Assertions
            logger.info("Performing assertions")
            assert (
                result["message"]
                == "AI interaction saved successfully for memory type: summarized memory"
            )
            assert result["session_id"] == mock_interaction_request["session_id"]
            assert "response" in result
            assert result["user_prompt_id"] == "test_prompt"

            logger.info("All assertions passed successfully")

        except Exception as e:
            logger.error(f"Test failed with error: {str(e)}")
            raise

    logger.info("Test completed successfully")


@pytest.mark.asyncio
async def test_summarymemory_error_handling(
    prompt_manager, mock_interaction_request, mock_user_prompt
):
    logger.info("\n" + "=" * 50)
    logger.info("Starting test_summarymemory_error_handling")
    logger.info("=" * 50)

    # Mock the method to raise an exception
    logger.info("Setting up mock method to raise exception")
    test_error = Exception("Test error")
    prompt_manager._fetch_and_cache_prompt_details = AsyncMock(side_effect=test_error)

    # Test error handling
    logger.info("Testing error handling")
    with pytest.raises(ValueError) as exc_info:
        await prompt_manager.summarymemory_save_log_ai_interaction_prompt(
            user_id="test_user",
            user_prompt_id="test_prompt",
            user_prompt=mock_user_prompt,
            interaction_request=mock_interaction_request,
        )

    logger.info(f"Caught expected exception: {str(exc_info.value)}")
    assert "An error occurred while processing AI interaction" in str(exc_info.value)

    logger.info("Test completed successfully")
