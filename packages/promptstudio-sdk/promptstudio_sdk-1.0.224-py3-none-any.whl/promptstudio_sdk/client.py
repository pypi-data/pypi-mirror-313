from typing import Dict, TypedDict, Optional
from .prompt import PromptManager


class ConfigDict(TypedDict):
    api_key: str
    env: str
    bypass: Optional[bool]
    is_logging: Optional[bool]


class PromptStudio(PromptManager):
    """
    Main client class for PromptStudio SDK
    Inherits all functionality from PromptManager
    """

    def __init__(self, config: ConfigDict):
        """
        Initialize the PromptStudio client

        Args:
            config: Dictionary containing:
                - 'api_key': API key
                - 'env': Environment ('test' or 'prod')
                - 'bypass': Optional boolean to bypass PromptStudio server
                - 'is_logging': Optional boolean to enable logging
        """
        super().__init__(config)
