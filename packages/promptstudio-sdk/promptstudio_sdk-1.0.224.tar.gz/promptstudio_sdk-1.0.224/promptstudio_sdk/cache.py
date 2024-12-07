from typing import Dict, List, Optional
import logging
from pathlib import Path
from .persistent_cache import PersistentCache

logger = logging.getLogger(__name__)


class CacheManager:
    _cache: Dict[str, Dict] = {}

    @classmethod
    def set_prompt_details(cls, prompt_id: str, details: Dict) -> None:
        """Store prompt details in cache with version info"""
        cls._cache[prompt_id] = details

    @classmethod
    def get_prompt_details(cls, prompt_id: str) -> Optional[Dict]:
        """Get prompt details from cache"""
        details = cls._cache.get(prompt_id)
        return details

    @classmethod
    def has_prompt_details(cls, prompt_id: str) -> bool:
        """Check if prompt details exist in cache"""
        return prompt_id in cls._cache

    @classmethod
    def print_cache_contents(cls) -> None:
        """Print all contents of the cache for debugging"""
        print("\n=== Cache Contents ===")
        if not cls._cache:
            print("Cache is empty")
        for key, value in cls._cache.items():
            print(f"\nKey: {key}")
            print(f"Value: {value}")

    @classmethod
    def delete_prompt_details(cls, cache_key: str):
        """Delete specific prompt details from cache"""
        # Delete both regular cache key and prompt_details cache key
        if cache_key in cls._cache:
            del cls._cache[cache_key]
        prompt_details_key = f"{cache_key}_prompt_details"
        if prompt_details_key in cls._cache:
            del cls._cache[prompt_details_key]

    @classmethod
    def delete_session(cls, session_id: str):
        """Delete all cache entries for a specific session"""
        keys_to_delete = [
            k
            for k in cls._cache.keys()
            if f"_{session_id}" in k or f"_{session_id}_prompt_details" in k
        ]
        for key in keys_to_delete:
            del cls._cache[key]

    @classmethod
    def delete_prompt(cls, prompt_id: str):
        """Delete all cache entries for a specific prompt"""
        keys_to_delete = [
            k
            for k in cls._cache.keys()
            if k.startswith(f"{prompt_id}_")
            or k.startswith(f"{prompt_id}_")
            and k.endswith("_prompt_details")
        ]
        for key in keys_to_delete:
            del cls._cache[key]


class InteractionCacheManager:
    _interaction_cache: Dict[str, Dict] = {}
    _user_messages: Dict[str, Dict] = {}
    _prompt_version_messages: Dict[str, List] = {}
    _persistent = PersistentCache()

    @classmethod
    def save_user_messages(cls, prompt_id: str, messages: Dict) -> None:
        """Save user messages with system message and variables"""

        cls._user_messages[prompt_id] = messages

    @classmethod
    def save_interaction(
        cls,
        session_id: str,
        interaction_data: Dict,
        prompt_id: str,
        version: str,
    ) -> None:
        """
        Save interaction with hierarchical tracking and message history.
        Maintains a hierarchical cache structure: prompt_id -> session_id -> version -> messages

        Args:
            session_id: Unique identifier for the chat session
            interaction_data: Dictionary containing messages and metadata for the interaction
            prompt_id: ID of the prompt being used
            version: Version of the prompt

        The method:
        1. Creates nested dictionaries for prompt_id, session_id and version if they don't exist
        2. Retrieves existing messages for the given prompt/session/version
        3. Appends new messages from interaction_data to existing messages
        4. Updates both in-memory cache and persistent storage with:
           - Combined message history
           - Last response timestamp
           - Memory type (defaults to "fullMemory")
           - Window size (defaults to 10)
        """

        # Initialize nested cache structure if needed
        if prompt_id not in cls._interaction_cache:
            cls._interaction_cache[prompt_id] = {}
            logger.debug(f"Created new prompt cache for {prompt_id}")

        # Initialize session if not exists
        if session_id not in cls._interaction_cache[prompt_id]:
            cls._interaction_cache[prompt_id][session_id] = {}
            logger.debug(f"Created new session cache for {session_id}")

        # Initialize version if not exists
        if version not in cls._interaction_cache[prompt_id][session_id]:
            cls._interaction_cache[prompt_id][session_id][version] = {
                "messages": [],
                "lastResponseAt": None,
            }
            logger.debug(f"Created new version cache for {version}")

        # Get existing messages
        existing_messages = cls._interaction_cache[prompt_id][session_id][version].get(
            "messages", []
        )

        # Add new messages to existing ones
        new_messages = interaction_data.get("messages", [])

        # Combine existing and new messages while maintaining order
        updated_messages = existing_messages + new_messages

        # Update cache with combined messages
        cls._interaction_cache[prompt_id][session_id][version].update(
            {
                "messages": updated_messages,
                "lastResponseAt": interaction_data["lastResponseAt"],
                "memory_type": interaction_data.get("memory_type", "fullMemory"),
                "window_size": interaction_data.get("window_size", 10),
            }
        )

        # Save to persistent storage
        cache_key = f"{prompt_id}_{session_id}"
        persistent_data = {
            "messages": updated_messages,
            "lastResponseAt": interaction_data["lastResponseAt"],
            "memory_type": interaction_data.get("memory_type", "fullMemory"),
            "window_size": interaction_data.get("window_size", 10),
        }
        cls._persistent.save(cache_key, persistent_data)

    @classmethod
    def get_interaction_history(
        cls, prompt_id: str, session_id: str, version: str
    ) -> Optional[Dict]:
        """Get interaction history with persistence"""
        # Try memory cache first
        history = (
            cls._interaction_cache.get(prompt_id, {}).get(session_id, {}).get(version)
        )

        # If not in memory, try persistent storage
        if not history:
            cache_key = f"{prompt_id}_{session_id}"
            history = cls._persistent.load(cache_key)
            if history:
                # Update memory cache
                if prompt_id not in cls._interaction_cache:
                    cls._interaction_cache[prompt_id] = {}
                if session_id not in cls._interaction_cache[prompt_id]:
                    cls._interaction_cache[prompt_id][session_id] = {}
                cls._interaction_cache[prompt_id][session_id][version] = history

        return history

    @classmethod
    def get_all_prompt_interactions(cls, prompt_id: str) -> Dict:
        """Get all interactions for a specific prompt across all sessions and versions"""
        interactions = cls._interaction_cache.get(prompt_id, {})
        return interactions

    @classmethod
    def clear_cache(cls) -> None:
        """Clear both memory and persistent cache"""
        cls._interaction_cache.clear()
        cls._user_messages.clear()
        cls._prompt_version_messages.clear()
        cls._persistent.clear()

    @classmethod
    def print_cache_contents(cls) -> None:
        """Print all contents of different caches for debugging"""
        print("\n=== Interaction Cache Contents ===")
        if not cls._interaction_cache:
            print("Interaction cache is empty")
        for prompt_id, sessions in cls._interaction_cache.items():
            print(f"\nPrompt ID: {prompt_id}")
            for session_id, versions in sessions.items():
                print(f"  Session ID: {session_id}")
                for version, data in versions.items():
                    print(f"    Version: {version}")
                    print(f"    Messages: {data['messages']}")
                    print(f"    Last Response At: {data['lastResponseAt']}")

        print("\n=== User Messages Cache Contents ===")
        if not cls._user_messages:
            print("User messages cache is empty")
        for key, value in cls._user_messages.items():
            print(f"\nPrompt ID: {key}")
            print(f"Messages: {value}")

    @classmethod
    def verify_cache_storage(
        cls, prompt_id: str, session_id: str, version: str
    ) -> Dict:
        """
        Verify cache storage for a specific prompt, session and version
        Returns a dictionary with cache verification details
        """
        verification_result = {
            "cache_exists": False,
            "message_count": 0,
            "last_message": None,
            "cache_details": None,
        }

        try:
            # Check if cache exists for this combination
            if (
                prompt_id in cls._interaction_cache
                and session_id in cls._interaction_cache[prompt_id]
                and version in cls._interaction_cache[prompt_id][session_id]
            ):

                cache_data = cls._interaction_cache[prompt_id][session_id][version]
                messages = cache_data.get("messages", [])

                verification_result.update(
                    {
                        "cache_exists": True,
                        "message_count": len(messages),
                        "last_message": messages[-1] if messages else None,
                        "cache_details": {
                            "lastResponseAt": cache_data.get("lastResponseAt"),
                            "total_interactions": len(messages)
                            // 2,  # user + assistant messages
                        },
                    }
                )

                logger.info(
                    f"Cache verification for prompt_id={prompt_id}, "
                    f"session_id={session_id}, version={version}: {verification_result}"
                )
            else:
                logger.warning(
                    f"No cache found for prompt_id={prompt_id}, "
                    f"session_id={session_id}, version={version}"
                )

        except Exception as e:
            logger.error(f"Error verifying cache: {str(e)}")
            verification_result["error"] = str(e)

        return verification_result

    @classmethod
    def delete_interaction(cls, prompt_id: str, session_id: str):
        """Delete specific interaction from cache"""
        cache_key = f"{prompt_id}_{session_id}"
        prompt_details_key = f"{cache_key}_prompt_details"

        # Clear from interaction cache
        if prompt_id in cls._interaction_cache:
            if session_id in cls._interaction_cache[prompt_id]:
                del cls._interaction_cache[prompt_id][session_id]

        # Clear from persistent cache
        cls._persistent.clear(cache_key)
        cls._persistent.clear(prompt_details_key)

    @classmethod
    def delete_session(cls, session_id: str):
        """Delete all interactions for a specific session"""
        # Clear from interaction cache
        for prompt_id in list(cls._interaction_cache.keys()):
            if session_id in cls._interaction_cache[prompt_id]:
                del cls._interaction_cache[prompt_id][session_id]

        # Clear from persistent cache
        cache_dir = Path("./persistent_cache")
        for cache_file in cache_dir.glob("*.pkl"):
            key = cache_file.stem  # Get filename without extension
            if f"_{session_id}" in key or f"_{session_id}_prompt_details" in key:
                cls._persistent.clear(key)

    @classmethod
    def delete_prompt(cls, prompt_id: str):
        """Delete all interactions for a specific prompt"""
        # Clear from interaction cache
        if prompt_id in cls._interaction_cache:
            del cls._interaction_cache[prompt_id]

        # Clear from persistent cache
        cache_dir = Path("./persistent_cache")
        for cache_file in cache_dir.glob("*.pkl"):
            key = cache_file.stem  # Get filename without extension
            if key.startswith(f"{prompt_id}_") or (
                key.startswith(f"{prompt_id}_") and key.endswith("_prompt_details")
            ):
                cls._persistent.clear(key)
