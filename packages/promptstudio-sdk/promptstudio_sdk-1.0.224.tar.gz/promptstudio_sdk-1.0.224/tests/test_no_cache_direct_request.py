import asyncio
import pytest
from promptstudio_sdk import PromptStudio

# Test configuration
TEST_CONFIG = {
    "api_key": "yLSjOm26OZCqFjMDXGBrZOKIC98qpYMv",
    "env": "test",
    "bypass": False,  # Enable bypass mode for direct AI platform calls
}


@pytest.fixture
def client():
    return PromptStudio(TEST_CONFIG)


@pytest.mark.asyncio
async def test_no_cache_direct_request_with_image():
    """Test direct AI request with image input and no caching"""
    client = PromptStudio(TEST_CONFIG)

    try:
        response = await client.chat_with_prompt(
            prompt_id="66f660e33e6e774719e30e93",
            user_message=[
                {
                    "type": "text",
                    "text": "Hello, I have a patient Narpat, check his face for symptoms",
                }
                # , {
                #     "type": "file",
                #     "file_url": {
                #         "url": "https://regionalneurological.com/wp-content/uploads/2019/08/AdobeStock_244803452.jpeg"
                #     },
                # },
            ],
            memory_type="fullMemory",
            window_size=2,
            session_id="",
            variables={},
            is_session_enabled=False,  # Disable session to use _no_cache_direct_ai_request
        )

        # Assertions
        assert response is not None
        assert "response" in response
        print("\nResponse from direct request:", response)

    except Exception as e:
        pytest.fail(f"Test failed with error: {str(e)}")


# @pytest.mark.asyncio
# async def test_no_cache_direct_request_with_variables():
#     """Test direct AI request with variables and no caching"""
#     client = PromptStudio(TEST_CONFIG)

#     try:
#         response = await client.chat_with_prompt(
#             prompt_id="66f660e33e6e774719e30e93",
#             user_message=[
#                 {
#                     "type": "text",
#                     "text": "Hello, I have a patient {{patient_name}}, check their face for symptoms",
#                 },
#                 {
#                     "type": "file",
#                     "file_url": {
#                         "url": "https://regionalneurological.com/wp-content/uploads/2019/08/AdobeStock_244803452.jpeg"
#                     },
#                 },
#             ],
#             memory_type="fullMemory",
#             window_size=2,
#             session_id="",
#             variables={"patient_name": "John Smith"},
#             is_session_enabled=False,
#         )

#         # Assertions
#         assert response is not None
#         assert "response" in response
#         print("\nResponse with variables:", response)

#     except Exception as e:
#         pytest.fail(f"Test failed with error: {str(e)}")


# @pytest.mark.asyncio
# async def test_no_cache_direct_request_text_only():
#     """Test direct AI request with text only and no caching"""
#     client = PromptStudio(TEST_CONFIG)

#     try:
#         response = await client.chat_with_prompt(
#             prompt_id="66f660e33e6e774719e30e93",
#             user_message=[
#                 {
#                     "type": "text",
#                     "text": "What are common symptoms of facial nerve palsy?",
#                 }
#             ],
#             memory_type="fullMemory",
#             window_size=2,
#             session_id="",
#             variables={},
#             is_session_enabled=False,
#         )

#         # Assertions
#         assert response is not None
#         assert "response" in response
#         print("\nResponse with text only:", response)

#     except Exception as e:
#         pytest.fail(f"Test failed with error: {str(e)}")


# @pytest.mark.asyncio
# async def test_no_cache_direct_request_with_version():
#     """Test direct AI request with specific version and no caching"""
#     client = PromptStudio(TEST_CONFIG)

#     try:
#         response = await client.chat_with_prompt(
#             prompt_id="66f660e33e6e774719e30e93",
#             user_message=[
#                 {
#                     "type": "text",
#                     "text": "Hello, I have a patient Narpat, check his face for symptoms",
#                 },
#                 {
#                     "type": "file",
#                     "file_url": {
#                         "url": "https://regionalneurological.com/wp-content/uploads/2019/08/AdobeStock_244803452.jpeg"
#                     },
#                 },
#             ],
#             memory_type="fullMemory",
#             window_size=2,
#             session_id="",
#             variables={},
#             version=1,  # Specify version
#             is_session_enabled=False,
#         )

#         # Assertions
#         assert response is not None
#         assert "response" in response
#         print("\nResponse with specific version:", response)

#     except Exception as e:
#         pytest.fail(f"Test failed with error: {str(e)}")


# @pytest.mark.asyncio
# async def test_no_cache_direct_request_error_handling():
#     """Test error handling in direct AI request with invalid prompt ID"""
#     client = PromptStudio(TEST_CONFIG)

#     with pytest.raises(Exception) as exc_info:
#         await client.chat_with_prompt(
#             prompt_id="invalid_prompt_id",  # Invalid prompt ID
#             user_message=[{"type": "text", "text": "Test message"}],
#             memory_type="fullMemory",
#             window_size=2,
#             session_id="",
#             variables={},
#             is_session_enabled=False,
#         )

#     assert exc_info.value is not None
#     print("\nError handling test passed with error:", str(exc_info.value))


if __name__ == "__main__":
    pytest.main(["-v", "test_no_cache_direct_request.py"])
