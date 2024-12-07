from typing import Dict, Any, TypedDict, Optional
import aiohttp
import logging
import json
import ssl
import certifi
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
    handlers=[logging.StreamHandler()],  # This ensures output goes to console
)
logger = logging.getLogger(__name__)


class ConfigDict(TypedDict):
    api_key: str
    env: str
    bypass: Optional[bool]
    is_logging: Optional[bool]


class Base:
    def __init__(self, config: ConfigDict):
        """
        Initialize the base class with configuration

        Args:
            config: Dictionary containing:
                - 'api_key': API key
                - 'env': Environment ('test' or 'prod')
                - 'bypass': Optional boolean to bypass PromptStudio server
                - 'is_logging': Optional boolean to enable logging
        """
        self.api_key = config["api_key"]
        self.env = config["env"]
        self.bypass = config.get("bypass", False)
        self.is_logging = config.get("is_logging", True)

        self.base_url = (
            "https://api.playground.promptstudio.dev/api/v1"
            if self.env == "test"
            else "https://api.promptstudio.dev/api/v1"
        )

    async def _request(
        self, endpoint: str, method: str = "GET", **kwargs
    ) -> Dict[str, Any]:
        """
        Make async HTTP requests to the API with proper SSL handling
        """
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

        # Create SSL context with proper certificate verification
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        # Log request details

        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=ssl_context)
            ) as session:
                if method.upper() == "POST" and "data" in kwargs:
                    if isinstance(kwargs["data"], str):
                        json_data = kwargs["data"]
                    else:
                        json_data = json.dumps(kwargs["data"])

                    async with session.post(
                        url, headers=headers, data=json_data
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
                else:
                    async with session.request(
                        method=method, url=url, headers=headers, **kwargs
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
        except aiohttp.ClientConnectorCertificateError as e:
            logger.error(f"SSL Certificate Error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Request Error: {str(e)}")
            raise
