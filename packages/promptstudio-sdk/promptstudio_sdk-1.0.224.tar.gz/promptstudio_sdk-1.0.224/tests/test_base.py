import pytest
import requests
from promptstudio_sdk.base import Base


def test_base_initialization():
    # Test initialization with test environment
    base = Base({"api_key": "test_key", "env": "test"})
    assert base.api_key == "test_key"
    assert base.env == "test"
    assert base.bypass == False  # Default should be False
    assert base.base_url == "https://api.playground.promptstudio.dev/api/v1"

    # Test initialization with prod environment
    base = Base({"api_key": "test_key", "env": "prod"})
    assert base.api_key == "test_key"
    assert base.env == "prod"
    assert base.bypass == False
    assert base.base_url == "https://api.promptstudio.dev/api/v1"

    # Test initialization with bypass
    base = Base({"api_key": "test_key", "env": "test", "bypass": True})
    assert base.bypass == True


@pytest.mark.asyncio
async def test_request_headers():
    base = Base({"api_key": "test_key", "env": "test"})

    # Mock the aiohttp ClientSession
    class MockResponse:
        async def json(self):
            return {"data": "test"}

        def raise_for_status(self):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    class MockClientSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def request(self, method, url, headers, **kwargs):
            # Test that headers are correctly set
            assert headers["Content-Type"] == "application/json"
            assert headers["x-api-key"] == "test_key"
            return MockResponse()

    # Replace aiohttp.ClientSession with our mock
    import aiohttp

    aiohttp.ClientSession = MockClientSession

    # Make a test request
    response = await base._request("/test")
    assert response == {"data": "test"}


@pytest.mark.asyncio
async def test_request_error_handling():
    base = Base({"api_key": "test_key", "env": "test"})

    # Mock aiohttp ClientSession for error
    class MockErrorResponse:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        def raise_for_status(self):
            raise aiohttp.ClientError("404 Client Error")

    class MockErrorSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def request(self, method, url, headers, **kwargs):
            return MockErrorResponse()

    # Replace aiohttp.ClientSession with our mock
    import aiohttp

    aiohttp.ClientSession = MockErrorSession

    # Test that the error is properly raised
    with pytest.raises(aiohttp.ClientError):
        await base._request("/test")
