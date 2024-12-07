from typing import Dict, Any, List, Union, Optional, Tuple

import requests
import logging
import uuid
import json
from datetime import datetime
from .base import Base
from .cache import CacheManager, InteractionCacheManager
import os
import hashlib
import tempfile
from pathlib import Path
import mimetypes
from bson import ObjectId

from openai import OpenAI
import openai

import anthropic
import google.generativeai as genai
from google.ai import generativelanguage as glm
from google.generativeai import types as generation_types

from google.ai.generativelanguage_v1beta.types import content
import httpx
import base64

import pickle
import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor

PROMPT_TO_GENERATE_SUMMARIZED_CONTENT = "Summarize the above conversation in a detailed, concise, and well-structured manner. ensuring the summary does not exceed 250 words. Capture the key points and context, including important questions, answers, and relevant follow-up, while avoiding unnecessary repetition. Present the summary in a well-structured paragraph, focusing on the most important content exchanged"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\n%(asctime)s - %(name)s - %(levelname)s - %(message)s\n",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,  # This ensures our configuration takes precedence
    handlers=[logging.StreamHandler()],  # This ensures output goes to console
)
logger = logging.getLogger(__name__)


class MessageQueue:
    def __init__(self, prompt_manager: "PromptManager"):
        self.queue = deque()
        self.is_processing = False
        self.prompt_manager = prompt_manager
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._shutdown = False

    async def add_message(self, message_data: Dict):
        """Add message to queue"""
        if not self._shutdown:
            self.queue.append(message_data)
            if not self.is_processing:
                asyncio.create_task(self._process_queue())

    async def _process_queue(self):
        """Process messages in queue"""
        if self.is_processing:
            return

        self.is_processing = True
        try:
            while self.queue and not self._shutdown:
                message_data = self.queue.popleft()
                try:
                    # Add error handling and validation
                    if not message_data.get("user_prompt_id"):
                        raise ValueError("Missing required field: user_prompt_id")

                    # Ensure the request URL is properly formatted
                    endpoint = f"/save_bypass_logs/{message_data['user_prompt_id']}"

                    # Create payload with error checking
                    payload = {
                        "user_message": message_data.get("user_message", ""),
                        "ai_response": message_data.get("ai_response", {}),
                        "session_id": message_data.get("session_id", ""),
                        "memory_type": message_data.get("memory_type", ""),
                        "window_size": message_data.get("window_size", 0),
                        "summarized_content": message_data.get(
                            "summarized_content", ""
                        ),
                        "request_from": message_data.get("request_from", "sdk"),
                    }

                    # Make the request with timeout
                    response = await self.prompt_manager.request(
                        endpoint,
                        method="POST",
                        json=payload,
                        timeout=30,  # Add reasonable timeout
                    )

                    if response:
                        logger.info(
                            f"Successfully stored message. Response: {response}"
                        )
                    else:
                        logger.warning("Received empty response from server")

                except Exception as e:
                    logger.error(f"Failed to store message: {str(e)}", exc_info=True)
                    # Optionally retry or handle specific errors

        finally:
            self.is_processing = False

    async def shutdown(self):
        """Gracefully shutdown the message queue"""
        self._shutdown = True
        # Wait for queue to empty
        while self.queue and self.is_processing:
            await asyncio.sleep(0.1)
        # Shutdown executor
        if self.executor:
            self.executor.shutdown(wait=True)


class PromptManager(Base):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        # Set up persistent cache directory
        self.cache_dir = Path("./persistent_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self._supported_memory_types = [
            "windowMemory",
            "fullMemory",
            "summarizedMemory",
        ]  # Define supported memory types
        self.message_queue = MessageQueue(self)  # Add message queue

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path for cache file"""
        return self.cache_dir / f"{cache_key}.pkl"

    def _save_to_persistent_cache(self, cache_key: str, data: Dict):
        """Save data to persistent cache"""
        try:
            cache_path = self._get_cache_path(cache_key)
            with open(cache_path, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving to persistent cache: {str(e)}")

    def _load_from_persistent_cache(self, cache_key: str) -> Optional[Dict]:
        """Load data from persistent cache"""
        try:
            cache_path = self._get_cache_path(cache_key)
            if cache_path.exists():
                with open(cache_path, "rb") as f:
                    data = pickle.load(f)
                return data
        except Exception as e:
            logger.error(f"Error loading from persistent cache: {str(e)}")
        return None

    async def request(self, endpoint: str, method: str, **kwargs):
        """Public method to make requests."""
        return await self._request(endpoint, method, **kwargs)

    def _print_persistent_cache_contents(self):
        """Print contents of persistent cache"""
        cache_files = list(self.cache_dir.glob("*.pkl"))

        for cache_file in cache_files:
            try:
                with open(cache_file, "rb") as f:
                    data = pickle.load(f)
            except Exception as e:
                logger.error(f"Error reading cache file {cache_file}: {str(e)}")

    async def get_all_prompts(self, folder_id: str) -> Dict:
        """
        Get all prompts for a given folder

        Args:
            folder_id: ID of the folder

        Returns:
            Dictionary containing prompt versions
        """
        response = await self._request(f"/{folder_id}")
        return response

    async def windowmemory_save_log_ai_interaction_prompt(
        self,
        user_prompt_id: str,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using window memory cache"""
        try:

            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())


            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")
            cache_key = f"{user_prompt_id}_{session_id}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )

            is_session_enabled = interaction_request.get("is_session_enabled")
            prompt_details["is_session_enabled"] = is_session_enabled

            # Get interaction history
            interaction_history = InteractionCacheManager.get_interaction_history(
                user_prompt_id, session_id, version
            )

            def_variables = prompt_details["variables"] if prompt_details else []
            default_variables = {}
            if (
                def_variables
                and (isinstance(def_variables, list) and len(def_variables) > 0)
                or (isinstance(def_variables, dict) and def_variables)
            ):

                default_variables = self.convert_data(def_variables)
                
            platform_name = prompt_details["ai_platform"]
            platform_key = prompt_details["platform_config"]["platformKey"]

            # Determine which variables to use based on the conditions
            if not interaction_request.get("variables"):
                # Condition 1: No variables given in interaction_request
                variables = default_variables
            else:
                # Condition 2 and 3: Check how many variables are provided
                provided_variables = interaction_request.get("variables")
                variables = {**default_variables}  # Start with default variables
                # Count how many variables are in default_variables
                default_keys = set(default_variables.keys())
                provided_keys = set(provided_variables.keys())
                if provided_keys.issubset(default_keys):
                    # Condition 3: All provided variables are in default_variables
                    variables = provided_variables
                else:
                    # Condition 2: Some variables are provided
                    for key in provided_keys:
                        if key in default_keys:
                            variables[key] = provided_variables[key]
                    # Add remaining default variables
                    for key in default_keys:
                        if key not in provided_keys:
                            variables[key] = default_variables[key]

            prompt_collection_msg = []
            messages = []
            window_size = interaction_request.get("window_size")
            if window_size % 2 != 0:
                window_size += 1

            # Add system message if platform is OpenAI
            if platform_name == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )
            if platform_name == "groq" or platform_name == "grok":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": prompt_details["system_prompt"],
                    }
                )
          
            # Add previous messages from history based on shot size
            if prompt_details and "messages" in prompt_details:

                published_messages = prompt_details["messages"]
                shot_size = interaction_request.get(
                    "shot", -1
                )  # Default to -1 for all messages

                if published_messages and shot_size != 0:
                    if shot_size > 0:
                        # Calculate number of messages to include (2 messages per shot)
                        messages_to_include = shot_size * 2
                        published_messages = published_messages[:messages_to_include]
                    # If shot_size is -1, use all messages (default behavior)
                    prompt_collection_msg.extend(published_messages)

            # Add previous messages within window size
            if interaction_history and interaction_history.get("messages"):
                # Get last N messages based on window size
                messages.extend(interaction_history["messages"])
                start_idx = max(
                    0, len(messages) - (window_size)
                )  # *2 for pairs of messages
                window_messages = messages[start_idx:]
                prompt_collection_msg.extend(window_messages)

            if platform_name == "claude":
                prompt_collection_msg = self.modify_messages_for_claude(
                    prompt_collection_msg
                )

                interaction_request["user_message"] = (
                    self.modify_new_user_message_for_claude(
                        interaction_request["user_message"]
                    )
                )

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": interaction_request["user_message"],
                }
            )
            
            prompt_details["system_prompt"] = self.replace_placeholders(prompt_details["system_prompt"], variables)
            # Replace placeholders in prompt_collection_msg
            prompt_collection_msg = self.replace_placeholders(prompt_collection_msg, variables)

            # Make AI platform request
            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details=prompt_details,
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
                platform_key=platform_key,
                variables=variables,
                prompt_id=user_prompt_id,
            )

            # if (
            #     platform_name == "claude"
            #     and prompt_details.get("is_session_enabled") is True
            # ):
            #     assistant_reply = response
            # elif (
            #     platform_name == "claude"
            #     and prompt_details.get("is_session_enabled") is False
            # ):
            #     assistant_reply = response["data"]["response"]
            # else:
            assistant_reply = response["response"]
            input_tokens = response["input_tokens"]
            output_tokens = response["output_tokens"]
            total_tokens = response["total_tokens"]

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{assistant_reply}"}],
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache with window memory configuration
            InteractionCacheManager.save_interaction(
                session_id=session_id,
                interaction_data={
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": "windowMemory",
                    "window_size": window_size,
                },
                prompt_id=user_prompt_id,
                version=version,
            )

            if self.is_logging:
    
                endpoint = f"/save_bypass_logs/{prompt_details['version_id']}"
                payload = {
                    "user_message": interaction_request["user_message"],
                    "ai_response": {"type": "text", "text": f"{assistant_reply}"},
                    "session_id": session_id,
                    "memory_type": "windowMemory",
                    "window_size": window_size,
                    "summarized_content": "",
                    "request_from": "python_sdk",
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                }
                response = await self.request(
                    endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )
                if response:
                    logger.info(f"Successfully stored message. Response: {response}")
                else:
                    logger.warning("Received empty response from server")


            if self.is_logging is False:

                endpoint = "/save_transaction_logs"
                payload = { 
                    "promptId":user_prompt_id,
                    "versionId":prompt_details["version_id"],
                    "platform":platform_name,
                    "model":prompt_details["model"],
                    "input_tokens":input_tokens,
                    "output_tokens":output_tokens,
                    "total_tokens":total_tokens,
                }
                response = await self.request(
                      endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )

            return {"response": assistant_reply,
                     "session_id": session_id,
                     "input_tokens": input_tokens,
                     "output_tokens": output_tokens,
                     "total_tokens": total_tokens}
                        
        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)


    def modify_new_user_message_for_claude(self, messages):
        """
        Process direct messages for Claude API format by converting file_url to base64 encoded images.
        Args:
            messages (list): List of direct messages containing potential image content
        Returns:
            list: Processed messages with images converted to Claude's format
        """
        # Define supported image types and their corresponding media types
        supported_media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".jfif": "image/jpeg",
            # '.webp': 'image/webp',
            # '.heic': 'image/heic',
            # '.heif': 'image/heif',
            # '.gif': 'image/gif'
        }
        for message in messages:
            if "type" in message and message["type"] == "file":
                # Fetch the image URL dynamically
                file_url = message["file_url"]["url"]
                # Extract file extension from URL
                _, file_extension = os.path.splitext(file_url.lower())
                # Check if file extension is supported
                if file_extension not in supported_media_types:
                    raise ValueError(
                        f"Unsupported image format: {file_extension}. "
                        f"Supported formats are: {', '.join(supported_media_types.keys())}"
                    )
                # Get the corresponding media type
                image_media_type = supported_media_types[file_extension]
                # Fetch the image data and encode it in base64
                image_data = base64.b64encode(httpx.get(file_url).content).decode(
                    "utf-8"
                )
                # Update the message structure to Claude format
                message["type"] = "image"
                message["source"] = {
                    "type": "base64",
                    "media_type": image_media_type,
                    "data": image_data,
                }
                # Remove the old 'file_url' key
                message.pop("file_url", None)
        return messages

    async def fullmemory_save_log_ai_interaction_prompt(
        self,
        user_prompt_id: str,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using cache memory"""
        try:
            # Generate session_id if not present
            session_id = interaction_request.get("session_id") or str(uuid.uuid4())

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")
            cache_key = f"{user_prompt_id}_{session_id}"
            prompt_details = CacheManager.get_prompt_details(cache_key)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )
                

            is_session_enabled = interaction_request.get("is_session_enabled")
            prompt_details["is_session_enabled"] = is_session_enabled

            # Get interaction history
            interaction_history = InteractionCacheManager.get_interaction_history(
                user_prompt_id, session_id, version
            )

            def_variables = prompt_details["variables"] if prompt_details else []
            default_variables = {}
            if (
                def_variables
                and (isinstance(def_variables, list) and len(def_variables) > 0)
                or (isinstance(def_variables, dict) and def_variables)
            ):
                default_variables = self.convert_data(def_variables)

            platform_name = prompt_details["ai_platform"]
            platform_key = prompt_details["platform_config"]["platformKey"]

            # Determine which variables to use based on the conditions
            if not interaction_request.get("variables"):
                # Condition 1: No variables given in interaction_request
                variables = default_variables
            else:
                # Condition 2 and 3: Check how many variables are provided
                provided_variables = interaction_request.get("variables")
                variables = {**default_variables}  # Start with default variables
                # Count how many variables are in default_variables
                default_keys = set(default_variables.keys())
                provided_keys = set(provided_variables.keys())
                if provided_keys.issubset(default_keys):
                    # Condition 3: All provided variables are in default_variables
                    variables = provided_variables
                else:
                    # Condition 2: Some variables are provided
                    for key in provided_keys:
                        if key in default_keys:
                            variables[key] = provided_variables[key]
                    # Add remaining default variables
                    for key in default_keys:
                        if key not in provided_keys:
                            variables[key] = default_variables[key]

            # Build message collection
            prompt_collection_msg = []

            # Add system message if platform is OpenAI
            if platform_name == "openai":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": [
                            {"type": "text", "text": prompt_details["system_prompt"]}
                        ],
                    }
                )
            if platform_name == "groq" or platform_name == "grok":
                prompt_collection_msg.append(
                    {
                        "role": "system",
                        "content": prompt_details["system_prompt"],
                    }
                )
            # # Add previous messages from history
            # if prompt_details and "messages" in prompt_details:

            #     published_messages = prompt_details["messages"]
            #     if published_messages:
            #         prompt_collection_msg.extend(published_messages)

            # Add previous messages from history based on shot size
            if prompt_details and "messages" in prompt_details:
                published_messages = prompt_details["messages"]
                shot_size = interaction_request.get(
                    "shot", -1
                )  # Default to -1 for all messages

                if published_messages and shot_size != 0:
                    if shot_size > 0:
                        # Calculate number of messages to include (2 messages per shot)
                        messages_to_include = shot_size * 2
                        published_messages = published_messages[:messages_to_include]
                    # If shot_size is -1, use all messages (default behavior)
                    prompt_collection_msg.extend(published_messages)

            # Add interaction messages from interaction history
            if interaction_history and interaction_history.get("messages"):
                prompt_collection_msg.extend(interaction_history["messages"])

            if platform_name == "claude":
                prompt_collection_msg = self.modify_messages_for_claude(
                    prompt_collection_msg
                )

                interaction_request["user_message"] = (
                    self.modify_new_user_message_for_claude(
                        interaction_request["user_message"]
                    )
                )

            # Add new user message
            prompt_collection_msg.append(
                {
                    "role": "user",
                    "content": interaction_request["user_message"],
                }
            )

            prompt_details["system_prompt"] = self.replace_placeholders(prompt_details["system_prompt"], variables)
            # Replace placeholders in prompt_collection_msg
            prompt_collection_msg = self.replace_placeholders(prompt_collection_msg, variables)

            response = await self._make_ai_platform_request(
                platform_name=platform_name,
                prompt_details=prompt_details,
                messages=prompt_collection_msg,
                system_message=prompt_details["system_prompt"],
                platform_key=platform_key,
                variables=variables,
                prompt_id=user_prompt_id,
            )
            
            # if (
            #     platform_name == "claude"
            #     and prompt_details.get("is_session_enabled") is True
            # ):
            #     assistant_reply = response
            # elif (
            #     platform_name == "claude"
            #     and prompt_details.get("is_session_enabled") is False
            # ):
            #     assistant_reply = response["data"]["response"]
            # else:
           
            assistant_reply = response["response"]
            input_tokens = response["input_tokens"]
            output_tokens = response["output_tokens"]
            total_tokens = response["total_tokens"]
           

            # Create new messages to save
            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": [{"type": "text", "text": f"{assistant_reply}"}],
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache with all required information
            InteractionCacheManager.save_interaction(
                session_id=session_id,
                interaction_data={
                    "messages": new_messages,
                    "lastResponseAt": current_time,
                    "memory_type": interaction_request.get("memory_type", "fullMemory"),
                    "window_size": interaction_request.get("window_size", 10),
                },
                prompt_id=user_prompt_id,
                version=version,
            )

            if self.is_logging:
            
                endpoint = f"/save_bypass_logs/{prompt_details['version_id']}"
                payload = {
                    "user_message": interaction_request["user_message"],
                    "ai_response": {"type": "text", "text": f"{assistant_reply}"},
                    "session_id": session_id,
                    "memory_type": "fullMemory",
                    "window_size": 0,
                    "summarized_content": "",
                    "request_from": "python_sdk",
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                    
                }
                response = await self.request(
                    endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )
                if response:
                    logger.info(f"Successfully stored message. Response: {response}")
                else:
                    logger.warning("Received empty response from server")

            if self.is_logging is False:

                endpoint = "/save_transaction_logs"
                payload = { 
                    "promptId":user_prompt_id,
                    "versionId":prompt_details["version_id"],
                    "platform":platform_name,
                    "model":prompt_details["model"],
                    "input_tokens":input_tokens,
                    "output_tokens":output_tokens,
                    "total_tokens":total_tokens,
                }
                
                
                response = await self.request(
                    endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )
              
            return {"response": assistant_reply, 
                    "session_id": session_id,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens}

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error(error_message)
            raise ValueError(error_message)
        

    def replace_placeholders(self, msg_list, variables):
        # Check if variables is empty
        if not variables:
            return msg_list  # Return original list if variables is empty
        # Handle different types of input
        if isinstance(msg_list, dict):
            # If input is a dictionary, recursively process each value
            return {
                k: self.replace_placeholders(v, variables) for k, v in msg_list.items()
            }
        elif isinstance(msg_list, list):
            # If input is a list, recursively process each item
            return [self.replace_placeholders(msg, variables) for msg in msg_list]
        elif isinstance(msg_list, str):
            # If input is a string, replace placeholders
            for key, value in variables.items():
                msg_list = msg_list.replace(f"{{{{{key}}}}}", str(value))
            return msg_list
        else:
            # For any other type, return unchanged
            return msg_list
        # The following code is for handling specific message structures
        # Create a new list to store the modified messages
        modified_msg_list = []
        for msg in msg_list:
            new_msg = msg.copy()  # Create a copy of the message to modify
            if isinstance(new_msg, dict) and "content" in new_msg:
                if isinstance(new_msg["content"], str):
                    # Handle string content
                    for key, value in variables.items():
                        new_msg["content"] = new_msg["content"].replace(
                            f"{{{{{key}}}}}", str(value)
                        )
                elif isinstance(new_msg["content"], list):
                    # Handle list of content
                    new_content = []
                    for content in new_msg["content"]:
                        new_content_item = content.copy()
                        if (
                            isinstance(new_content_item, dict)
                            and "text" in new_content_item
                        ):
                            for key, value in variables.items():
                                new_content_item["text"] = new_content_item[
                                    "text"
                                ].replace(f"{{{{{key}}}}}", str(value))
                        new_content.append(new_content_item)
                    new_msg["content"] = new_content
            modified_msg_list.append(new_msg)
        return modified_msg_list  # Return the new list with modified messages

    def convert_data(self, data):
        # Create an empty dictionary to hold the converted data
        result = {}
        # Iterate through each item in the input data
        for item in data:
            # Extract 'name' and 'value' and add them to the result dictionary
            if "name" in item and "value" in item:
                result[item["name"]] = item["value"]
        return result

    def modify_messages_for_claude(self, messages):
        """
        Process images in messages for Claude API format by converting file_url to base64 encoded images.
        Args:
            messages (list): List of messages containing potential image content
            Returns:
            list: Processed messages with images converted to Claude's format
        """
        # Define supported image types and their corresponding media types
        supported_media_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".jfif": "image/jpeg",
            # '.webp': 'image/webp',
            # '.heic': 'image/heic',
            # '.heif': 'image/heif',
            # '.gif': 'image/gif'
        }
        for message in messages:
            if "content" in message:
                for content in message["content"]:
                    if content.get("type") == "file":
                        # Fetch the image URL dynamically
                        file_url = content["file_url"]["url"]
                        # Extract file extension from URL
                        _, file_extension = os.path.splitext(file_url.lower())
                        # Check if file extension is supported
                        if file_extension not in supported_media_types:
                            raise ValueError(
                                f"Unsupported image format: {file_extension}. "
                                f"Supported formats are: {', '.join(supported_media_types.keys())}"
                            )
                        # Get the corresponding media type
                        image_media_type = supported_media_types[file_extension]
                        # Fetch the image data and encode it in base64
                        image_data = base64.b64encode(
                            httpx.get(file_url).content
                        ).decode("utf-8")
                        # Update the content structure
                        content["type"] = "image"
                        content["source"] = {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        }
                        # Remove the old 'file_url' key
                        content.pop("file_url", None)
        return messages

    def update_messages_collection(self, platform_name, system_message, old_messages):
        messages_collection = []
        # Add system message if platform is not Claude
        if platform_name == "openai":
            system_content = [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": system_message}],
                }
            ]
            messages_collection.extend(system_content)
        if platform_name == "groq" or platform_name == "grok":
            system_content = [
                {
                    "role": "system",
                    "content": system_message,
                }
            ]
            messages_collection.extend(system_content)

        if old_messages and len(old_messages) > 0:
            for message in old_messages:
                # Extract only the 'role' and 'content' fields
                simplified_message = {
                    "role": message["role"],
                    "content": message["content"],
                }
                messages_collection.append(simplified_message)

        return messages_collection

    async def summarizedmemory_save_log_ai_interaction_prompt(
        self,
        user_prompt_id: str,
        interaction_request: Dict,
    ) -> Dict:
        """Process and save AI interaction using summary memory cache"""
        try:

            session_type, session_id = self._fetch_session_id(interaction_request)
            cache_key = f"{user_prompt_id}_{session_id}"
            cache_key_prompt_details = f"{user_prompt_id}_{session_id}_prompt_details"

            # Get version (either from request or fetch latest)
            version = interaction_request.get("version")

            # First fetch and cache prompt details
            prompt_details = CacheManager.get_prompt_details(cache_key_prompt_details)

            if not prompt_details:
                # Fetch and cache if not found
                prompt_details = await self._fetch_and_cache_prompt_details(
                    user_prompt_id, session_id, version
                )

            prompt_details["is_session_enabled"] = interaction_request.get("is_session_enabled", True)

            system_message = (
                prompt_details["system_prompt"]
                if prompt_details.get("system_prompt")
                else ""
            )

            old_messages = []
            # Get messages from history based on shot size
            if prompt_details:
                shot_size = interaction_request.get("shot", -1)  # Default to -1 for all messages

                if prompt_details.get("messages") and shot_size != 0:
                    messages = prompt_details.get("messages", [])
                    if shot_size > 0:
                        # Calculate number of messages to include (2 messages per shot)
                        messages_to_include = shot_size * 2
                        old_messages = messages[:messages_to_include]
                    else:
                        # If shot_size is -1, use all messages
                        old_messages = messages

            variables = (prompt_details["variables"] if prompt_details.get("variables") else {})
            default_variables = convert_variables_data(variables)
            variables = merge_default_and_provided_variables(interaction_request, default_variables)

            result = await self.get_summarized_content(prompt_id=user_prompt_id,session_id=session_id)

            # Initialize summarized_content
            summarized_content = ""
            if result["status"] == "success":
                summarized_content = result["summarized_content"]
            

            new_user_message = interaction_request["user_message"]
            if prompt_details["ai_platform"] == "claude":
                new_user_message = self.modify_new_user_message_for_claude(new_user_message)

            messages_collection = self.update_messages_collection(prompt_details["ai_platform"], system_message, old_messages)

            if session_type == "new_session":
                messages_collection.extend(
                    [
                        {
                            "role": "user",
                            "content": new_user_message,
                        }
                    ]
                )

            elif session_type == "existing_session":
                content = [
                    {
                        "type": "text",
                        "text": f"Summary of previous AI Interaction: {summarized_content}\n\nNew user message that needs to be responded is in next message:",
                        
                    }
                ]

                for message in new_user_message:
                    if isinstance(message, dict) and message.get("type") == "file":
                        content.append(message)
                    else:
                        content.append(message)

                if prompt_details["ai_platform"] == "gemini":
                    messages_collection.extend(
                        [
                            {
                                "role": "user",
                                "content": new_user_message,
                            }
                        ]
                    )

                else:

                    messages_collection.extend(
                        [
                            {
                                "role": "user",
                                "content": content,
                            }
                        ]
                    )
            
            platform_key = prompt_details["platform_config"]["platformKey"]
            system_message = self.replace_placeholders(system_message, variables)
            messages_collection = self.replace_placeholders(messages_collection, variables)

            response = await self._make_ai_platform_request(
                platform_name=prompt_details["ai_platform"],
                prompt_details=prompt_details,
                messages=messages_collection,
                system_message=system_message,
                platform_key=platform_key,
                variables=variables,
                prompt_id=user_prompt_id,
            )
            
            # Get both response and summary in one call
            if prompt_details["ai_platform"] == "claude":

                # if prompt_details.get("is_session_enabled") is True:
                #     response1 = response
                # else:
                #     response1 = response["data"]["response"]
                response1 = response["response"]
                input_tokens0 = response["input_tokens"]
                output_tokens0 = response["output_tokens"]
                total_tokens0 = response["total_tokens"]

                # response1 = response["content"][0]["text"]
                # Generate summary using the same messages plus the new response
                summary_messages = messages_collection.copy()
                summary_messages.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": response1}],
                    }
                )
                summary_messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": PROMPT_TO_GENERATE_SUMMARIZED_CONTENT,
                            }
                        ],
                    }
                )

                # Add summary request to the same API call
                summary_response = await self._make_ai_platform_request(
                    platform_name=prompt_details["ai_platform"],
                    prompt_details=prompt_details,
                    messages=summary_messages,
                    system_message=system_message,
                    platform_key=platform_key,
                    variables=variables,
                    prompt_id=user_prompt_id,
                )

                # if (
                #     prompt_details.get("is_session_enabled") is True
                #     and prompt_details["ai_platform"] == "claude"
                # ):
                #     new_summarized_content = summary_response
                # elif (
                #     prompt_details["ai_platform"] == "claude"
                #     and prompt_details.get("is_session_enabled") is False
                # ):
                #     new_summarized_content = summary_response["data"]["response"]
                # else:
                    # new_summarized_content = summary_response["response"]
                
                new_summarized_content = summary_response["response"]
                input_tokens1 = summary_response["input_tokens"]
                output_tokens1 = summary_response["output_tokens"]
                total_tokens1 = summary_response["total_tokens"]
                    
                ai_response = {"type": "text", "text": response1}
            else:
                response1 = response["response"]
                input_tokens0 = response["input_tokens"]
                output_tokens0 = response["output_tokens"]
                total_tokens0 = response["total_tokens"]
                
                # Generate summary using the same messages plus the new response
                summary_messages = messages_collection.copy()
                summary_messages.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": f"{response1}"}],
                    }
                )
                summary_messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": PROMPT_TO_GENERATE_SUMMARIZED_CONTENT,
                            }
                        ],
                    }
                )

                # Add summary request to the same API call
                summary_response = await self._make_ai_platform_request(
                    platform_name=prompt_details["ai_platform"],
                    prompt_details=prompt_details,
                    messages=summary_messages,
                    system_message=system_message,
                    platform_key=platform_key,
                    variables=variables,
                    prompt_id=user_prompt_id,
                )
                new_summarized_content = summary_response["response"]
                input_tokens1 = summary_response["input_tokens"]
                output_tokens1 = summary_response["output_tokens"]
                total_tokens1 = summary_response["total_tokens"]
                ai_response = {"type": "text", "text": response1}

            current_time = datetime.now().isoformat()
            new_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "user",
                    "content": interaction_request["user_message"],
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": ai_response,
                    "requestFrom": interaction_request.get("request_from", "sdk"),
                    "initiatedAt": current_time,
                },
            ]

            # Save to cache in background
            interaction_data = {
                "messages": new_messages,
                "lastResponseAt": current_time,
                "memory_type": "summarizedMemory",
                "summarized_content": new_summarized_content,
            }

            # Create background task for caching
            asyncio.create_task(
                self._background_cache_save(cache_key, interaction_data)
            )

            if self.is_logging:
               
                input_tokens = input_tokens0 + input_tokens1
                output_tokens = output_tokens0 + output_tokens1
                total_tokens = total_tokens0 + total_tokens1
               
                endpoint = f"/save_bypass_logs/{prompt_details['version_id']}"
                payload = {
                    "user_message": interaction_request["user_message"],
                    "ai_response": {"type": "text", "text": f"{response1}"},
                    "session_id": session_id,
                    "memory_type": "summarizedMemory",
                    "window_size": 0,
                    "summarized_content": f"{new_summarized_content}",
                    "request_from": "python_sdk",
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens,
                }
                response = await self.request(
                    endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )
                if response:
                    logger.info(f"Successfully stored message. Response: {response}")
                else:
                    logger.warning("Received empty response from server")


            if self.is_logging is False:

                input_tokens = input_tokens0 + input_tokens1
                output_tokens = output_tokens0 + output_tokens1
                total_tokens = total_tokens0 + total_tokens1

                endpoint = "/save_transaction_logs"
                payload = { 
                    "promptId":user_prompt_id,
                    "versionId":prompt_details["version_id"],
                    "platform":prompt_details["ai_platform"],
                    "model":prompt_details["model"],
                    "input_tokens":input_tokens,
                    "output_tokens":output_tokens,
                    "total_tokens":total_tokens,
                }
                response = await self.request(
                      endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )

            return {"response": response1, 
                    "session_id": session_id,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": total_tokens}

        except Exception as e:
            error_message = (
                f"An error occurred while processing AI interaction: {str(e)}"
            )
            logger.error("\nERROR OCCURRED:")
            logger.error(error_message)
            logger.error("Cache state at error:")
            # self._print_persistent_cache_contents()
            raise ValueError(error_message)


    async def _background_cache_save(self, cache_key: str, interaction_data: Dict):
        """Background task to save cache data with error handling"""
        try:
            self._save_to_persistent_cache(cache_key, interaction_data)
        except Exception as e:
            logger.error(f"Error saving to cache in background: {str(e)}")


    async def _fetch_and_cache_prompt_details(
        self, prompt_id: str, session_id: str, version: Optional[str] = None
    ) -> Dict:
        """
        Fetch prompt details from PromptStudio

        Args:
            prompt_id: ID of the prompt
            session_id: Session ID
            version: Optional version number (if None, will use null in request)

        Returns:
            Dictionary containing prompt details
        """
        try:
            # Clean the prompt_id
            prompt_id = prompt_id.strip()

            # Prepare request body with proper version format and stringify
            request_body = json.dumps({"version": float(version) if version else None})

            # Make request to version_data endpoint with proper headers
            response = await self._request(
                f"/fetch/prompt/version_data/{prompt_id}",
                method="POST",
                data=request_body,  # Use data instead of json for stringified content
            )
            
            if not response.get("data") or not response["data"].get("result"):
                logger.error(f"Invalid response format for prompt_id: {prompt_id}")
                raise ValueError("Invalid response format from API")

            # Extract data from response
            result = response["data"]["result"]
            prompt = result["prompt"]
            version_id = prompt["_id"]
            ai_platform = prompt["aiPlatform"]
            messages = result["messages"]
            platform_config = result.get("platformConfig", {})
            variables = messages.get("variable", {})
            

            # Extract and format the prompt details
            prompt_details = {
                "ai_platform": ai_platform["platform"],
                "model": ai_platform["model"],
                "system_prompt": messages.get("systemMessage", ""),
                "temperature": ai_platform["temp"],
                "max_tokens": ai_platform["max_tokens"],
                "messages": messages.get("messages", []),
                "top_p": ai_platform["top_p"],
                "frequency_penalty": ai_platform["frequency_penalty"],
                "presence_penalty": ai_platform["presence_penalty"],
                "response_format": ai_platform["response_format"],
                "version": prompt["version"],
                "platform_config": platform_config,  # Include platform config if needed
                "variables": variables,
                "version_id": version_id,
            }

            # Cache the prompt details
            cache_key = f"{prompt_id}_{session_id}"
            CacheManager.set_prompt_details(cache_key, prompt_details)

            return prompt_details

        except Exception as e:
            logger.error(f"Error in _fetch_and_cache_prompt_details: {str(e)}")
            raise

    def modify_messages_for_openai(self, messages):
        """Convert file types to image_url format for OpenAI"""
        modified_messages = []
        supported_extensions = [".png", ".jpeg", ".jpg", ".webp", ".jfif"]

        for message in messages:
            modified_content = []
            for content in message.get("content", []):
                if content.get("type") == "file" and content.get("file_url", {}).get(
                    "url"
                ):
                    image_url = content["file_url"]["url"]
                    _, extension = os.path.splitext(image_url)
                    if extension.lower() not in supported_extensions:
                        raise ValueError(
                            f"Unsupported image extension: {extension}. "
                            "We currently support PNG (.png), JPEG (.jpeg and .jpg), "
                            "WEBP (.webp), and JFIF (.jfif)"
                        )
                    modified_content.append(
                        {"type": "image_url", "image_url": {"url": image_url}}
                    )
                else:
                    modified_content.append(content)

            modified_messages.append(
                {"role": message["role"], "content": modified_content}
            )
        return modified_messages
    

    async def _make_openai_request(self, prompt_details: Dict, payload: Dict, platform_key :str, prompt_id: str) -> Dict:
        """Make a direct request to OpenAI"""
        # Get OpenAI API key from environment when in bypass mode
        openai_api_key = platform_key
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY  variable is required , bypass mode is true. which is set while publishing the prompt"
            )

        # Extract messages from payload
        messages = payload.get("user_message", [])
        # Process each message and handle file types
        messages = self.modify_messages_for_openai(messages)
        

        try:
            response = openai_interaction(
                secret_key=openai_api_key,  
                model=prompt_details["model"],
                messages=messages,
                temperature=prompt_details.get("temp", 0.7),
                max_tokens=prompt_details["max_tokens"],
                top_p=prompt_details.get("top_p", 0.5),
                frequency_penalty=prompt_details.get("frequency_penalty", 0.7),
                presence_penalty=prompt_details.get("presence_penalty", 0.3),
                response_format=prompt_details.get("response_format"),
            )
            
            if prompt_details.get("is_session_enabled") is True:
                return response

            else:
                return {
                        "message": "AI interactions log saved successfully",
                        "data": {
                            "message": "AI interaction saved successfully ",
                            "user_prompt_id": prompt_id,
                            "response": response["response"],
                            "input_tokens": response["input_tokens"],
                            "output_tokens": response["output_tokens"],
                            "total_tokens": response["total_tokens"],
                            "session_id": None,
                        },
                    }
        except Exception as e:
            logger.error(f"Error making OpenAI request: {str(e)}")
            raise



    async def _make_anthropic_request(
        self, prompt_details: Dict, payload: Dict, platform_key
    ) -> Dict:
        """Make a direct request to Anthropic"""
        user_message = next(
            (msg for msg in payload["user_message"] if msg["type"] == "text"), None
        )
        if not user_message:
            logger.error("No text message found in payload")
            raise ValueError("Text message is required for Anthropic requests")

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": platform_key,
                    "Content-Type": "application/json",
                },
                json={
                    "model": prompt_details["model"],
                    "messages": [
                        {
                            "role": "system",
                            "content": prompt_details["system_prompt"],
                        },
                        {"role": "user", "content": user_message["text"]},
                    ],
                    "max_tokens": prompt_details["max_tokens"],
                },
            )
            response.raise_for_status()
            data = response.json()
            return {"response": data["content"][0]["text"]}
        except Exception as e:
            logger.error(f"Error making Anthropic request: {str(e)}")
            raise
    
    
    async def claude_interaction_chat_with_prompt(
        self,
        secret_key,
        model,
        max_tokens,
        temperature,
        messages,
        system_message,
        is_session_enabled,
    ):
        messages = remove_id_from_messages(messages)
        messages = self.modify_messages_for_claude(messages)
        client = anthropic.Anthropic(api_key=secret_key)

        try:
            if system_message and system_message.strip():
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                    system=system_message,  # Pass system message as a separate parameter
                )
            else:
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                )
            if not response.content:
                logger.warning(
                    "Empty response content from Claude API. This may occur if the API returned an empty array."
                )
                return {
                    "response": "No content was generated. Please try again or rephrase your query."
                }
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            print(f"""
════════════════════  Claude Token Usage  ══════════════════════╗
  Input Tokens:    {input_tokens:6,d}                                  
  Output Tokens:   {output_tokens:6,d}                                  
  Total Tokens:    {total_tokens:6,d}                                  
════════════════════════════════════════════════════════════════╝
""")
            assistant_reply = response.content[0].text
            ai_response = {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_reply}],
            }
            return { "response": assistant_reply, 
                    "input_tokens": input_tokens, 
                    "output_tokens": output_tokens, 
                    "total_tokens": total_tokens }

        except Exception as e:
            raise ValueError(f"API interaction error: {str(e)}")


    async def _no_cache_direct_ai_request(
        self,
        prompt_id: str,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        variables: Dict[str, str],
        version: Optional[int] = None,
        shot: Optional[int] = -1,
        memory_type: Optional[str] = None,
    ) -> Dict:
        """Handle direct AI platform requests without caching"""
        # return await self._direct_ai_request(prompt_id, session_id, payload)
        try:
            # Clean the prompt_id
            prompt_id = prompt_id.strip()
            requested_variables = variables
            # Prepare request body with proper version format and stringify
            request_body = json.dumps({"version": float(version) if version else None})

            # Make request to version_data endpoint with proper headers
            response = await self._request(
                f"/fetch/prompt/version_data/{prompt_id}",
                method="POST",
                data=request_body,  # Use data instead of json for stringified content
            )

            if not response.get("data") or not response["data"].get("result"):
                raise ValueError("Invalid response format from API")
            
            # Extract data from response
            result = response["data"]["result"]
            prompt = result["prompt"]
            version_id = prompt["_id"]
            ai_platform = prompt["aiPlatform"]
            system_message = self.clean_system_message(result["messages"]["systemMessage"])
            messages = result["messages"]["messages"]
            variables = result["messages"].get("variable", {})
         
           
            # Add shot-based message slicing
            shot_size = shot if shot is not None else -1  # Use provided shot or default to -1
            if shot_size == 0:
                messages = []  # Return empty messages list if shot is 0
            elif messages:  # Only process if messages exist and shot isn't 0
                if shot_size > 0:
                    # Calculate number of messages to include (2 messages per shot)
                    messages_to_include = shot_size * 2
                    messages = messages[:messages_to_include]
                # If shot_size is -1, use all messages (default behavior)

            if ai_platform["platform"] == "openai":
                messages.insert(0,{"role": "system", "content": [{"type": "text", "text": system_message}]})

            if ai_platform["platform"] == "groq" or ai_platform["platform"] == "grok":
                messages.insert(0,{"role": "system", "content": system_message})

            messages.extend([{"role": "user", "content": user_message}])

            platform_config = result.get("platformConfig", {})
            
            # Extract and format the prompt details
            prompt_details = {
                "ai_platform": ai_platform["platform"],
                "model": ai_platform["model"],
                "system_prompt": system_message,
                "temperature": ai_platform["temp"],
                "max_tokens": ai_platform["max_tokens"],
                "messages": messages,  # Use the extended messages
                "top_p": ai_platform["top_p"],
                "frequency_penalty": ai_platform["frequency_penalty"],
                "presence_penalty": ai_platform["presence_penalty"],
                "response_format": ai_platform["response_format"],
                "version": prompt["version"],
                "platform_config": platform_config,  # Include platform config if needed
                "variables": variables,
                "is_session_enabled": False,
            }
            def_variables = prompt_details["variables"] if prompt_details else []
            default_variables = {}
            if (
                def_variables
                and (isinstance(def_variables, list) and len(def_variables) > 0)
                or (isinstance(def_variables, dict) and def_variables)
            ):
                default_variables = self.convert_data(def_variables)


            # Determine which variables to use based on the conditions
            if not requested_variables:
                # Condition 1: No variables given in interaction_request
                variables = default_variables
            else:
                # Condition 2 and 3: Check how many variables are provided
                provided_variables = requested_variables
                variables = {**default_variables}  # Start with default variables
                # Count how many variables are in default_variables
                default_keys = set(default_variables.keys())
                provided_keys = set(provided_variables.keys())
                if provided_keys.issubset(default_keys):
                    # Condition 3: All provided variables are in default_variables
                    variables = provided_variables
                else:
                    # Condition 2: Some variables are provided
                    for key in provided_keys:
                        if key in default_keys:
                            variables[key] = provided_variables[key]
                    # Add remaining default variables
                    for key in default_keys:
                        if key not in provided_keys:
                            variables[key] = default_variables[key]
            
            system_message = self.replace_placeholders(system_message, variables)
            messages = self.replace_placeholders(messages, variables)

            platform_response = await self._make_ai_platform_request(
                platform_name=ai_platform["platform"],  # Use platform string directly
                prompt_details=prompt_details,
                messages=messages,
                system_message=system_message,
                platform_key=platform_config["platformKey"],
                variables=variables,
                prompt_id=prompt_id,
            )
            
            if self.is_logging:
            
                endpoint = f"/save_bypass_logs/{version_id}"
                payload = {
                    "user_message": user_message,
                    "ai_response": {"type": "text", "text": f"{platform_response['data']['response']}"},
                    "session_id": "",
                    "memory_type": memory_type,
                    "window_size": 0,
                    "summarized_content": "",
                    "request_from": "python_sdk",
                    "input_tokens": platform_response["data"]["input_tokens"],
                    "output_tokens": platform_response["data"]["output_tokens"],
                    "total_tokens": platform_response["data"]["total_tokens"],
                    
                }
                response = await self.request(
                    endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )
                if response:
                    logger.info(f"Successfully stored message. Response: {response}")
                else:
                    logger.warning("Received empty response from server")

            if self.is_logging is False:

                endpoint = "/save_transaction_logs"
                payload = { 
                    "promptId":prompt_id,
                    "versionId":version_id,
                    "platform":prompt_details["ai_platform"],
                    "model":prompt_details["model"],
                    "input_tokens":platform_response["data"]["input_tokens"],
                    "output_tokens":platform_response["data"]["output_tokens"],
                    "total_tokens":platform_response["data"]["total_tokens"],
                }
                response = await self.request(
                      endpoint,
                    method="POST",
                    json=payload,
                    timeout=30,  # Add reasonable timeout
                )
                
            return platform_response    
        except Exception as e:
            logger.error(f"Error in _no_cache_direct_ai_request: {str(e)}")
            raise

   

    async def _get_existing_summarized_content(
        self, interaction_history: Dict, session_id: str, version: str
    ) -> str:
        """Get existing summarized content from interaction history"""
        if (
            interaction_history
            and interaction_history.get("memory_type") == "summarizedMemory"
            and "summarized_content" in interaction_history
        ):
            return interaction_history["summarized_content"]
        return ""


    async def chat_with_prompt(
        self,
        prompt_id: str,
        user_message: List[Dict[str, Union[str, Dict[str, str]]]],
        memory_type: str,
        window_size: int,
        session_id: str,
        variables: Dict[str, str],
        version: Optional[int] = None,
        is_session_enabled: Optional[bool] = True,
        shot: Optional[int] = -1,
    ) -> Dict[str, str]:
        """
        Chat with a specific prompt

        Args:
            prompt_id: ID of the prompt
            user_message: List of message dictionaries
            memory_type: Type of memory ('fullMemory', 'windowMemory', or 'summarizedMemory')
            window_size: Size of the memory window
            session_id: Session identifier
            variables: Dictionary of variables
            version: Optional version number

        Returns:
            Dictionary containing the response
        """
        if memory_type not in self._supported_memory_types:
            raise ValueError(
                f"Unsupported memory type: {memory_type}. Supported types are: {', '.join(self._supported_memory_types)}"
            )

        payload = {
            "user_message": user_message,
            "memory_type": memory_type,
            "window_size": window_size,
            "session_id": session_id,
            "env": self.env,
            "request_from": "python_sdk",
            "variables": variables,
            "version": version,
            "shot": shot,
            "is_session_enabled": is_session_enabled,
        }

        no_bypass_payload = {
            "user_message": user_message,
            "memory_type": memory_type,
            "window_size": window_size,
            "session_id": session_id,
            "variables": variables,
            "request_from": "python_sdk",
            "shot": shot,
        }

        if version is not None:
            payload["version"] = version
            no_bypass_payload["version"] = version

        try:
            if self.bypass:

                if is_session_enabled is False:
                    return await self._no_cache_direct_ai_request(
                        prompt_id, user_message, variables, version, shot ,memory_type
                    )
                if memory_type == "summarizedMemory":
                    response = await self.summarizedmemory_save_log_ai_interaction_prompt(
                        prompt_id, payload
                    )

                elif memory_type == "windowMemory":
                    response = await self.windowmemory_save_log_ai_interaction_prompt(
                        prompt_id, payload
                    )
                
                elif memory_type == "fullMemory":
                    response = await self.fullmemory_save_log_ai_interaction_prompt(
                        prompt_id, payload
                    )
                
                else:
                    raise ValueError(
                        f"Invalid memory type: {memory_type}. Supported types are: {', '.join(self._supported_memory_types)}"
                    )

            else:
                response = await self._request(
                    f"/chat_with_prompt_version/{prompt_id}",
                    method="POST",
                    json=no_bypass_payload,
                )

            if self.bypass:
                return {
                    "message": "AI interactions log saved successfully",
                    "data": {
                            "message": f"AI interaction saved successfully for memory type: {memory_type}",
                            "user_prompt_id": prompt_id,
                            "response": response["response"],
                            "input_tokens": response["input_tokens"],
                            "output_tokens": response["output_tokens"],
                            "total_tokens": response["total_tokens"],
                            "session_id": response["session_id"],
                            
                    },
                }
            else:
                return response
        except Exception as e:
            logger.error(f"Error in chat_with_prompt: {str(e)}")
            raise


    async def _make_ai_platform_request(
        self,
        platform_name: str,
        prompt_details: Dict,
        messages: List[Dict],
        system_message: str,
        platform_key: str,
        variables: Dict,
        prompt_id: str,
    ) -> Dict:
        """
        Make request to the appropriate AI platform

        Args:
            platform_name: Name of the AI platform (openai, anthropic, etc.)
            prompt_details: Dictionary containing prompt configuration
            messages: List of messages to send
            system_message: System message to use

        Returns:
            Dictionary containing the response
        """
        
        if system_message:
            system_message = self.clean_system_message(system_message)

        try:
            if platform_name.lower() == "openai":
                return await self._make_openai_request(prompt_details, {"user_message": messages}, platform_key, prompt_id)
            
            elif platform_name.lower() == "claude":
                if not platform_key:
                    raise ValueError(
                        "CLAUDE_API_KEY  is required when using Claude, which is set while publishing the prompt. bypass mode is true"
                    )
                response = await self.claude_interaction_chat_with_prompt(
                    secret_key=platform_key,
                    model=prompt_details["model"],
                    max_tokens=prompt_details["max_tokens"],
                    temperature=prompt_details["temperature"],
                    messages=messages,
                    system_message=system_message,
                    is_session_enabled=prompt_details.get("is_session_enabled"),
                )
                
                if prompt_details.get("is_session_enabled") is True:
                    return response
                
                else:
                    return {
                        "message": "AI interactions log saved successfully",
                        "data": {
                            "message": "AI interaction saved successfully ",
                            "user_prompt_id": prompt_id,
                            "response": response["response"],
                            "input_tokens": response["input_tokens"],
                            "output_tokens": response["output_tokens"],
                            "total_tokens": response["total_tokens"],
                            "session_id": None,
                        },
                    }
            
            elif platform_name.lower() == "gemini":
                if not platform_key:
                    raise ValueError(
                        "GEMINI_API_KEY  is required when using Gemini, which is set while publishing the prompt. bypass mode is true"
                    )

                gemini_response = gemini_interaction_chat_with_prompt(
                    secret_key=platform_key,  
                    model=prompt_details["model"],
                    messages=messages,
                    system_message=system_message,
                    temperature=prompt_details.get("temp", 0.7),
                    max_output_tokens=prompt_details.get("max_tokens", 1000),
                    top_p=prompt_details.get("top_p", 0.8),
                    top_k=prompt_details.get("top_k", 40),
                    response_format=prompt_details.get("response_format"),
                )
                
                # return gemini_response
                if prompt_details.get("is_session_enabled") is True:
                    return gemini_response
                else:
                    return {
                        "message": "AI interactions log saved successfully",
                        "data": {
                                "message": "AI interaction saved successfully for memory type: full memory",
                                "user_prompt_id": prompt_id,
                                "response": gemini_response["response"],
                                "input_tokens": gemini_response["input_tokens"],
                                "output_tokens": gemini_response["output_tokens"],
                                "total_tokens": gemini_response["total_tokens"],
                                "session_id": None,
                        },
                    }
            elif platform_name.lower() == "groq" or platform_name.lower() == "grok":
                response = openai_supported_models_interaction(
                secret_key=platform_key,
                model=prompt_details["model"],
                messages=messages,
                temperature=prompt_details["temperature"],
                max_tokens=prompt_details["max_tokens"],
                top_p=prompt_details["top_p"],
                frequency_penalty=prompt_details["frequency_penalty"],
                presence_penalty=prompt_details["presence_penalty"],
                response_format=prompt_details["response_format"],
                platform= platform_name
            )
                if prompt_details.get("is_session_enabled"):
                    return response

                else:
                    return {
                        "message": "AI interactions log saved successfully",
                        "data": {
                            "message": "AI interaction saved successfully ",
                            "user_prompt_id": prompt_id,
                            "response": response["response"],
                            "input_tokens": response["input_tokens"],
                            "output_tokens": response["output_tokens"],
                            "total_tokens": response["total_tokens"],
                            "session_id": None,
                        },
                    }
            else:
                error_msg = f"Unsupported AI platform: {platform_name}"
                logger.error(error_msg)
                raise ValueError(error_msg)

        except Exception as e:
            logger.error(f"Error in _make_ai_platform_request: {str(e)}")
            raise


    def _fetch_session_id(self, interaction_request: Dict) -> Tuple[str, str]:
        """
        Determine session type and get session ID from interaction request

        Args:
            interaction_request: Dictionary containing the interaction request

        Returns:
            Tuple containing (session_type, session_id)
        """
        session_id = interaction_request.get("session_id", "")
        if not session_id:
            new_session = str(ObjectId())
            return "new_session", new_session
        else:
            return "existing_session", session_id


    async def get_summarized_content(
        self, prompt_id: str, session_id: str
    ) -> Dict[str, Any]:
        """
        Fetch summarized content for a specific prompt session.

        Args:
            prompt_id: ID of the prompt
            session_id: Session identifier

        Returns:
            Dictionary containing the summarized content and status
        """
        try:

            # Generate cache key
            cache_key = f"{prompt_id}_{session_id}"

            # Try to load from persistent cache
            cached_data = self._load_from_persistent_cache(cache_key)

            if cached_data and "summarized_content" in cached_data:
                return {
                    "status": "success",
                    "summarized_content": cached_data["summarized_content"],
                    "memory_type": cached_data.get("memory_type", "summarizedMemory"),
                    "session_id": session_id,
                }

            return {
                "status": "not_found",
                "message": "No summarized content found for this session",
                "session_id": session_id,
            }

        except Exception as e:
            error_message = f"Error fetching summarized content: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "message": error_message,
                "session_id": session_id,
            }

    def clean_system_message(self, system_message):
        """Clean the system message by removing comment blocks."""
        if not system_message:
            return None
        in_comment_block = False
        cleaned_lines = []
        for line in system_message.split("\n"):
            stripped_line = line.strip()
            # Check for comment block start
            if stripped_line.startswith("```comment"):
                in_comment_block = True
                continue
            # Check for comment block end
            if stripped_line == "```" and in_comment_block:
                in_comment_block = False
                continue
            # Add line only if we're not in a comment block
            if not in_comment_block:
                cleaned_lines.append(line.rstrip())
        return "\n".join(cleaned_lines)

    def clear_cache(
        self, session_id: Optional[str] = None, prompt_id: Optional[str] = None
    ):
        """
        Clear cache memory from both persistent storage and local cache managers.
        """
        try:
            cleared_items = []

            if session_id and prompt_id:
                # Clear specific session and prompt from persistent cache
                cache_key = f"{prompt_id}_{session_id}"
                prompt_details_key = f"{cache_key}_prompt_details"

                # Clear regular cache file
                cache_path = self._get_cache_path(cache_key)
                if cache_path.exists():
                    cache_path.unlink()
                    cleared_items.append("persistent cache")

                # Clear prompt details cache file
                details_cache_path = self._get_cache_path(prompt_details_key)
                if details_cache_path.exists():
                    details_cache_path.unlink()
                    cleared_items.append("persistent prompt details cache")

                # Clear from CacheManager
                CacheManager.delete_prompt_details(cache_key)
                cleared_items.append("prompt cache")

                # Clear from InteractionCacheManager
                InteractionCacheManager.delete_interaction(prompt_id, session_id)
                cleared_items.append("interaction cache")

                return {
                    "status": "success",
                    "message": f"Cache cleared for session {session_id} and prompt {prompt_id}",
                    "cleared": cleared_items,
                }

            # ... existing code for clearing based on session_id or prompt_id only ...

        except Exception as e:
            error_message = f"Error clearing cache: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "message": error_message,
                "cleared": cleared_items,
            }


def convert_object_ids(data):
    if isinstance(data, dict):
        return {k: convert_object_ids(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_object_ids(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime):
        return data.isoformat()  # Convert datetime to ISO format string
    else:
        return data


def openai_interaction(
    secret_key,
    model,
    messages,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
    response_format,
):
    """Make a request to OpenAI API"""
    # Set the OpenAI API key
    client = OpenAI(api_key=secret_key)
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_format=response_format,
            timeout=50000,
        )
        
        # Extract token usage from response
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

    
        print(f"""
    ══════════════════════ OpenAI Token Usage ══════════════════════╗
    Input Tokens:    {input_tokens:6,d}                                  
    Output Tokens:   {output_tokens:6,d}                                  
    Total Tokens:    {total_tokens:6,d}                                  
    ════════════════════════════════════════════════════════════════╝
    """)
        
        # Get the response content using the new API format
        assistant_reply = response.choices[0].message.content.strip()

        return {
            "response": assistant_reply,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise


def format_messages_for_gemini(messages, system_message=None):
    formatted_messages = []

    for i, msg in enumerate(messages):
        role = msg.get("role")
        content = msg.get("content")

        if isinstance(content, list):
            text_content = " ".join(
                [
                    (
                        part.get("text", "")
                        if isinstance(part.get("text"), str)
                        else json.dumps(part.get("text", ""))
                    )
                    for part in content
                    if part.get("type") == "text"
                ]
            )
        elif isinstance(content, str):
            text_content = content
        else:
            text_content = json.dumps(content)

        if i == 0 and system_message:
            text_content = f"{system_message}\n\n{text_content}"

        formatted_messages.append(
            {
                "role": "user" if role in ["user", "system"] else "model",
                "parts": [{"text": text_content}],
            }
        )

    return formatted_messages


def create_response_schema(payload: dict) -> content.Schema:
    def create_property_schema(prop):
        if isinstance(prop["type"], list):
            # Handle multiple types
            #  return content.Schema(
            #     type=content.Type.UNION,
            return glm.Content.Schema(
                type=glm.Content.Type.STRING,
                items=[
                    create_property_schema({"type": t})
                    for t in prop["type"]
                    if t != "null"
                ],
            )
        elif prop["type"] == "string":
            return content.Schema(type=content.Type.STRING)
        elif prop["type"] == "integer":
            return content.Schema(type=content.Type.INTEGER)
        elif prop["type"] == "number":
            return content.Schema(type=content.Type.NUMBER)
        elif prop["type"] == "boolean":
            return content.Schema(type=content.Type.BOOLEAN)
        elif prop["type"] == "array":
            if "items" in prop:
                return content.Schema(
                    type=content.Type.ARRAY, items=create_property_schema(prop["items"])
                )
            return content.Schema(type=content.Type.ARRAY)
        elif prop["type"] == "object":
            return create_response_schema(prop)
        else:
            return content.Schema(
                type=content.Type.STRING
            )  # Default to string for unknown types

    properties = {}
    for key, value in payload["properties"].items():
        properties[key] = create_property_schema(value)

    required = payload.get("required", [])
    return content.Schema(
        type=content.Type.OBJECT, properties=properties, required=required
    )


def gemini_interaction_chat_with_prompt(
    secret_key,
    model,
    messages,
    system_message,
    temperature,
    max_output_tokens,
    top_p,
    top_k,
    response_format
):
    genai.configure(api_key=secret_key)

    if system_message and system_message.strip():
        gemini_model = genai.GenerativeModel(
            model_name=model, system_instruction=system_message
        )
    else:
        gemini_model = genai.GenerativeModel(model_name=model)

    if response_format["type"] == "text":
        response_schema = None
        response_mime_type = "text/plain"
    else:
        try:
            response_schema = create_gemini_schema(response_format)
            response_mime_type = "application/json"
        except Exception as e:
            raise ValueError(f"Invalid JSON schema")

    generated_history = convert_messages_to_gemini_format(messages)

    # Prepare the message to send
    last_message_parts = generated_history[-1]["parts"]

    # Check if there is any text in the last message parts
    if not any(isinstance(part, str) and part.strip() for part in last_message_parts):
        # If no text is found, add a default text message
        last_message_parts = [""] + last_message_parts

    chat = gemini_model.start_chat(history=generated_history)

    try:

        response = chat.send_message(
            last_message_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_output_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                response_schema=response_schema,
                response_mime_type=response_mime_type,
            ),
        )

         # Extract token usage
        usage_metadata = response.usage_metadata
        input_tokens = usage_metadata.prompt_token_count
        output_tokens = usage_metadata.candidates_token_count
        total_tokens = usage_metadata.total_token_count
        print(f"""  
════════════════════  Gemini Token Usage  ══════════════════════╗
  Input Tokens:    {input_tokens:6,d}                             
  Output Tokens:   {output_tokens:6,d}                             
  Total Tokens:    {total_tokens:6,d}                             
════════════════════════════════════════════════════════════════╝
""")
        # Check if we have a valid response
        if response is None:
            raise ValueError("No valid response received from Gemini API")

        # The last response will be the model's reply to the most recent user message
        if response_mime_type == "text/plain":
            assistant_reply = response.text

        else:

            assistant_reply = response.candidates[0].content.parts[0].text
            assistant_reply = json.loads(assistant_reply)

        # assistant_reply = json.loads(assistant_reply)
        return {"response": assistant_reply ,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                }
    
    except genai.types.generation_types.BlockedPromptException as e:
        raise ValueError(f"Gemini API error: The prompt was blocked. Reason: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in Gemini interaction: {str(e)}")
        raise ValueError(f"Unexpected error occurred: {str(e)}")

def openai_supported_models_interaction(
    secret_key,
    model,
    messages,
    temperature,
    max_tokens,
    top_p,
    frequency_penalty,
    presence_penalty,
    response_format,
    platform
):
    
    messages = modify_messages_openai_supported_models(messages)
    client = OpenAI(api_key=secret_key)
    

    if platform == "groq":
        client = OpenAI(
            api_key=secret_key ,
            base_url="https://api.groq.com/openai/v1"
            )
      
    if platform == "grok":
        client = OpenAI(
            api_key=secret_key ,
            base_url="https://api.x.ai/v1"
            )

        
    # Call the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        timeout=50000,
    )
    
    # Extract token usage from response
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    if platform == "groq":
        print(f"""
    ══════════════════════  Groq Token Usage  ══════════════════════╗
    Input Tokens:    {input_tokens:6,d}                                  
    Output Tokens:   {output_tokens:6,d}                                  
    Total Tokens:    {total_tokens:6,d}                                  
    ════════════════════════════════════════════════════════════════╝
    """)
    if platform == "grok":
        print(f"""
    ══════════════════════  Grok Token Usage  ══════════════════════╗
    Input Tokens:    {input_tokens:6,d}                                  
    Output Tokens:   {output_tokens:6,d}                                  
    Total Tokens:    {total_tokens:6,d}                                  
    ════════════════════════════════════════════════════════════════╝
    """)
        
    assistant_reply = response.choices[0].message.content.strip()
    
    return {
            "response": assistant_reply,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }
    

def create_gemini_schema(response_dict: Dict[str, Any]) -> genai.protos.Schema:
    """
    Convert any dictionary into a Gemini response schema format.

    Args:
        response_dict (dict): Input dictionary to convert

    Returns:
        genai.protos.Schema: Gemini schema format
    """

    def _process_value(value: Any) -> genai.protos.Schema:
        if isinstance(value, dict):
            if "type" in value:
                # Handle OpenAPI/JSON schema style definitions
                schema_type = value["type"].upper()
                properties = {}
                required = []

                if schema_type == "OBJECT" and "properties" in value:
                    properties = {
                        k: _process_value(v) for k, v in value["properties"].items()
                    }
                    required = value.get("required", [])
                elif schema_type == "ARRAY" and "items" in value:
                    return genai.protos.Schema(
                        type=genai.protos.Type.ARRAY,
                        items=_process_value(value["items"]),
                    )

                schema = genai.protos.Schema(
                    type=getattr(genai.protos.Type, schema_type),
                    properties=properties,
                    required=required,
                )

                # Handle enums if present
                if "enum" in value:
                    schema = genai.protos.Schema(
                        type=genai.protos.Type.STRING, enum=value["enum"]
                    )

                # Handle description if present
                if "description" in value:
                    schema.description = value["description"]

                return schema
            else:
                # Handle nested dictionary without type specification
                return genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={k: _process_value(v) for k, v in value.items()},
                )
        elif isinstance(value, list):
            if value:
                return genai.protos.Schema(
                    type=genai.protos.Type.ARRAY, items=_process_value(value[0])
                )
            return genai.protos.Schema(
                type=genai.protos.Type.ARRAY,
                items=genai.protos.Schema(type=genai.protos.Type.STRING),
            )
        elif isinstance(value, bool):
            return genai.protos.Schema(type=genai.protos.Type.BOOLEAN)
        elif isinstance(value, int):
            return genai.protos.Schema(type=genai.protos.Type.INTEGER)
        elif isinstance(value, float):
            return genai.protos.Schema(type=genai.protos.Type.NUMBER)
        else:
            return genai.protos.Schema(type=genai.protos.Type.STRING)

    # Process the root schema
    return _process_value(response_dict)


def convert_messages_to_gemini_format(messages):
    gemini_messages = []
    for message in messages:
        role = "user" if message["role"] == "user" else "model"
        parts = []

        for content in message["content"]:
            if content["type"] == "text":
                parts.append(content["text"])
            elif content["type"] == "file":
                parts.append(upload_file_to_gemini(file_url=content["file_url"]["url"]))

        gemini_messages.append({"role": role, "parts": parts})

    return gemini_messages

def modify_messages_openai_supported_models(messages):
        modified_messages = []
        supported_extensions = ['.png', '.jpeg', '.jpg', '.webp', '.jfif']
        for message in messages:
            # Handle assistant messages differently
            if message["role"] == "assistant":
                # Extract text content directly from the message
                if isinstance(message["content"], list) and len(message["content"]) > 0:
                    # If content is a list with type/text structure, extract just the text
                    text_content = " ".join(
                        content["text"] for content in message["content"] 
                        if content["type"] == "text" and "text" in content
                    )
                    modified_messages.append({
                        "role": "assistant",
                        "content": text_content
                    })
                else:
                    # If content is already a string, use it directly
                    modified_messages.append({
                        "role": "assistant",
                        "content": message["content"]
                    })
                continue

            # Handle system messages (which are direct strings)
            if message["role"] == "system":
                modified_messages.append({
                    "role": "system",
                    "content": message["content"]  # Use the string content directly
                })
                continue

            # Handle other message types (primarily user) with existing logic
            if isinstance(message["content"], list):
                modified_content = []
                for content in message["content"]:
                    if content["type"] == "file" and content["file_url"]["url"]:
                        image_url = content["file_url"]["url"]
                        _, extension = os.path.splitext(image_url)
                        if extension not in supported_extensions:
                            raise ValueError(f"Unsupported image extension: {extension}. We currently support PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and JFIF (.jfif)")
                        modified_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        })
                    else:
                        modified_content.append(content)
                modified_messages.append({
                    "role": message["role"],
                    "content": modified_content
                })
            else:
                # Handle case where content is a direct string
                modified_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
                
        return modified_messages


def upload_file_to_gemini(file_url):

    with tempfile.TemporaryDirectory() as tempdir:
        tempfiles = Path(tempdir)
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.content

        # Generate file name and path
        name = file_url.split("/")[-1]
        hash = hashlib.sha256(data).hexdigest()
        path = tempfiles / hash

        # Write data to file
        path.write_bytes(data)

        print("Uploading:", file_url)
        mime_type = identify_mime_type(file_url)
        file_content = genai.upload_file(path, mime_type=mime_type)
        return file_content


def identify_mime_type(file_url):
    # Extract the file extension from the URL
    _, file_extension = os.path.splitext(file_url)
    file_extension = file_extension.lower()

    # Define custom mappings for specific file types
    custom_mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".jfif": "image/jpeg",
        ".webp": "image/webp",
        ".heic": "image/heic",
        ".heif": "image/heif",
        ".wav": "audio/wav",
        ".mp3": "audio/mp3",
        ".aiff": "audio/aiff",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
    }

    # Check if the file extension is in our custom mappings
    if file_extension in custom_mime_types:
        return custom_mime_types[file_extension]

    # If not in custom mappings, use mimetypes library as a fallback
    mime_type, _ = mimetypes.guess_type(file_url)

    # If mimetypes library couldn't determine the type, return a default
    if mime_type is None:
        return "application/octet-stream"

    return mime_type


# Helper methods for summary memory
SUMMARY_PROMPT = """Please provide a concise summary of the conversation so far, 
highlighting the key points and important context that would be relevant for continuing the discussion."""


def process_ai_response_by_format(get_ai_response, response_format):
    # Ensure get_ai_response is a string
    if not isinstance(get_ai_response, str):
        get_ai_response = json.dumps(get_ai_response)

    # Remove any surrounding quotes
    get_ai_response = get_ai_response.strip('"')

    # Process based on response_format type
    if response_format.get("type") == "text":
        # For text type, ensure it's a string
        try:
            # If it's valid JSON, convert it to a string
            parsed = json.loads(get_ai_response)
            if isinstance(parsed, (dict, list)):
                content = json.dumps(parsed)
            else:
                content = str(parsed)
        except json.JSONDecodeError:
            # If it's not valid JSON, use it as is
            content = get_ai_response
    elif response_format.get("type") == "object":
        # For object type, ensure it's a valid JSON object
        try:
            content = json.loads(get_ai_response)
            if not isinstance(content, dict):
                # If it's not a dict, wrap it in a dict
                content = {"content": content}
        except json.JSONDecodeError:
            # If it's not valid JSON, wrap it in a dict
            content = {"content": get_ai_response}
    else:
        # Default to treating it as text
        content = str(get_ai_response)

    # Return the processed response in the required format
    return {"role": "assistant", "content": [{"type": "text", "text": content}]}


async def _generate_summary(
    self, messages: list, prompt_details: Dict, interaction_request: Dict
) -> str:
    """Generate a summary of the conversation"""
    try:
        # Make request to AI platform for summary
        response = await self._make_ai_platform_request(
            platform_name=prompt_details["ai_platform"],
            prompt_details=prompt_details,
            messages=messages,
            system_message=self.SUMMARY_PROMPT,
        )

        return response["response"]
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise ValueError(f"Failed to generate summary: {str(e)}")


def convert_variables_data(data):
    # Create an empty dictionary to hold the converted data
    result = {}

    # Iterate through each item in the input data
    for item in data:
        # Extract 'name' and 'value' and add them to the result dictionary
        if "name" in item and "value" in item:
            result[item["name"]] = item["value"]

    return result


def merge_default_and_provided_variables(
    interaction_request: Dict, default_variables: Dict
) -> Dict:
    """
    Merge provided variables with default variables

    Args:
        interaction_request: Dictionary containing the interaction request
        default_variables: Dictionary containing default variables

    Returns:
        Dictionary containing merged variables
    """
    # Get variables from interaction request, defaulting to empty dict
    provided_variables = interaction_request.get("variables", {})

    if not provided_variables:
        return default_variables

    variables = {**default_variables}
    default_keys = set(default_variables.keys())
    provided_keys = set(provided_variables.keys())

    if provided_keys.issubset(default_keys):
        return provided_variables

    for key in provided_keys:
        if key in default_keys:
            variables[key] = provided_variables[key]
    for key in default_keys:
        if key not in provided_keys:
            variables[key] = default_variables[key]

    return variables


def remove_id_from_messages(messages):
    """
    Remove both '_id' and 'id' fields from messages while preserving other fields.

    Args:
        messages (list): List of message dictionaries

    Returns:
        list: Cleaned messages without '_id' and 'id' fields
    """
    cleaned_messages = []
    for message in messages:
        cleaned_message = {
            k: v
            for k, v in message.items()
            if k not in ["_id", "id", "env", "requestFrom", "initiatedAt"]
        }
        cleaned_messages.append(cleaned_message)
    return cleaned_messages
