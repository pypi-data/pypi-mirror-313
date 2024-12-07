import pytest
import os
import time
import logging
from openai import RateLimitError
from promptstudio_sdk.prompt import PromptManager
from promptstudio_sdk.cache import CacheManager, InteractionCacheManager
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@pytest.fixture
def prompt_manager():
    logger.info("Initializing test prompt manager")
    return PromptManager({"api_key": "test_key", "env": "test"})


@pytest.fixture
def prompt_manager_with_bypass():
    logger.info("Initializing prompt manager with bypass using OpenAI API key")
    return PromptManager(
        {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "env": "test",
            "bypass": True,
        }
    )


@pytest.mark.asyncio
async def test_get_all_prompts(prompt_manager):
    logger.info("Testing get_all_prompts functionality")

    async def mock_request(endpoint, method="GET", **kwargs):
        logger.debug(f"Mock request to endpoint: {endpoint} with method: {method}")
        assert endpoint == "/test_folder"
        assert method == "GET"
        return {"data": {"versions": []}}

    prompt_manager._request = mock_request
    response = await prompt_manager.get_all_prompts("test_folder")
    logger.info("Successfully retrieved all prompts")
    assert response == {"data": {"versions": []}}


@pytest.mark.asyncio
async def test_chat_with_prompt_bypass(prompt_manager_with_bypass):
    logger.info("Starting chat_with_prompt_bypass test")

    # Skip test if no API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not set in environment, skipping test")
        pytest.skip("OPENAI_API_KEY not set in environment")

    # Mock the fetch prompt details request with correct response structure
    async def mock_request(endpoint, method="GET", **kwargs):
        logger.debug(f"Mock request to endpoint: {endpoint} with method: {method}")

        # Handle latest version endpoint
        if "latest_version" in endpoint:
            return {
                "message": "Latest version fetched successfully",
                "data": {"latest_version": 1.3},
            }
        # Handle version data endpoint
        elif "version_data" in endpoint:
            return {
                "message": "Prompt data fetched successfully",
                "data": {
                    "status_code": 200,
                    "detail": "Prompt data fetched successfully",
                    "result": {
                        "prompt": {
                            "version": 1.2,
                            "aiPlatform": {
                                "_id": "672f03c90139bac78b597f1d",
                                "platform": "openai",
                                "model": "gpt-3.5-turbo",
                                "temp": 1,
                                "max_tokens": 1000,
                                "top_p": 0.5,
                                "frequency_penalty": 0.5,
                                "presence_penalty": 0.5,
                                "top_k": 1,
                                "response_format": {"type": "text"},
                            },
                            "isPublished": False,
                            "isImageSupport": False,
                            "isAudioSupport": False,
                            "_id": "672f03c40139bac78b597f1b",
                        },
                        "messages": {
                            "_id": "672f03c90139bac78b597f1e",
                            "promptsId": "672f03c40139bac78b597f1b",
                            "messages": [],
                            "systemMessage": "You are a helpful assistant",
                            "variable": [],
                            "createdAt": "2024-11-09T12:10:09.495000",
                            "lastResponseAt": "2024-11-09T12:10:09.495000",
                        },
                        "projectId": "672f0309796a316334f16c11",
                        "folderId": "672f0309796a316334f16c12",
                        "promptId": "672f0309796a316334f16c13",
                    },
                },
            }
        return {}

    prompt_manager_with_bypass._request = mock_request

    # Create mock OpenAI response
    class MockChoice:
        def __init__(self, message):
            self.message = message

    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice({"content": "Hello! How can I help you today?"})]

    # Mock OpenAI interaction
    def mock_openai_interaction(**kwargs):
        return MockResponse()

    # Replace the real OpenAI interaction with our mock
    original_openai_interaction = openai.chat.completions.create
    openai.chat.completions.create = mock_openai_interaction

    try:
        response = await prompt_manager_with_bypass.chat_with_prompt(
            prompt_id="671f7ea3895439853685b020",
            user_message=[
                {"role": "user", "content": [{"type": "text", "text": "Hello"}]}
            ],
            memory_type="fullMemory",
            window_size=10,
            session_id="test_session",
            variables={},
        )

        logger.info(f"Successfully received response from OpenAI: {response}")
        assert "response" in response
        assert isinstance(response["response"], str)
        assert len(response["response"]) > 0

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

    finally:
        # Restore original OpenAI function
        openai.chat.completions.create = original_openai_interaction


@pytest.mark.asyncio
async def test_fullmemory_save_log_ai_interaction(prompt_manager_with_bypass):
    logger.info("Testing fullmemory_save_log_ai_interaction_prompt")

    # Set up user messages in cache
    test_prompt_id = "test_prompt_123"
    InteractionCacheManager.save_user_messages(
        test_prompt_id,
        {
            "systemMessage": "You are a helpful assistant",
            "variable": {"name": "John", "company": "Acme"},
            "messages": [],
        },
    )

    # Mock the fetch prompt details request
    async def mock_request(endpoint, method="GET", **kwargs):
        if "latest_version" in endpoint:
            return {
                "message": "Latest version fetched successfully",
                "data": {"latest_version": 1.3},
            }
        return {
            "data": {
                "result": {
                    "prompt": {
                        "aiPlatform": {
                            "platform": "gemini",
                            "model": "gemini-pro",
                            "temp": 0.7,
                            "max_tokens": 150,
                            "top_p": 0.5,
                            "top_k": 40,
                            "response_format": {"type": "text"},
                        }
                    },
                    "messages": {
                        "systemMessage": "You are a helpful assistant",
                        "messages": [],
                    },
                }
            }
        }

    prompt_manager_with_bypass._request = mock_request

    # Mock Gemini response
    class MockPart:
        def __init__(self, text):
            self.text = text

    class MockCandidate:
        def __init__(self, content):
            self.content = content

    class MockResponse:
        def __init__(self, candidates):
            self.candidates = candidates

    def mock_generate_content(*args, **kwargs):
        content = type("Content", (), {"parts": [MockPart("Hello! I'm here to help.")]})
        return MockResponse([type("Candidate", (), {"content": content})()])

    # Mock Gemini model
    class MockGenerativeModel:
        def __init__(self, model_name, system_instruction=None):
            self.model_name = model_name
            self.system_instruction = system_instruction

        def generate_content(self, *args, **kwargs):
            return mock_generate_content()

    # Replace Gemini's GenerativeModel with our mock
    import google.generativeai as genai

    original_model = genai.GenerativeModel
    genai.GenerativeModel = MockGenerativeModel

    try:
        response = (
            await prompt_manager_with_bypass.fullmemory_save_log_ai_interaction_prompt(
                user_id="test_user",
                user_prompt_id=test_prompt_id,
                user_prompt={
                    "platform": "gemini",
                    "model": "gemini-pro",
                    "temp": 0.7,
                    "max_tokens": 150,
                    "top_p": 0.5,
                    "top_k": 40,
                    "response_format": {"type": "text"},
                    "system_prompt": "You are a helpful assistant",
                },
                interaction_request={
                    "user_message": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": "Hello!"}],
                        }
                    ],
                    "memory_type": "fullMemory",
                    "window_size": 10,
                    "session_id": "test_session",
                    "variables": {},
                    "env": "test",
                    "request_from": "sdk",
                },
            )
        )

        # Verify response
        assert "message" in response
        assert "user_prompt_id" in response
        assert "response" in response
        assert "session_id" in response

        # Verify cache state
        cached_interaction = InteractionCacheManager.get_interaction(
            response["session_id"]
        )
        assert cached_interaction is not None
        assert "messages" in cached_interaction
        assert len(cached_interaction["messages"]) == 2

    finally:
        # Clean up
        InteractionCacheManager.clear_cache()
        genai.GenerativeModel = original_model
