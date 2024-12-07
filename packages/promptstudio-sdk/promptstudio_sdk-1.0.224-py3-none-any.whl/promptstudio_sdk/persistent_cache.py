import json
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class PersistentCache:
    """Handles persistent storage of cache data"""

    def __init__(self, storage_dir: str = ".cache"):
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save(self, key: str, data: Any) -> None:
        """Save data to persistent storage"""
        try:
            file_path = os.path.join(self.storage_dir, f"{key}.json")
            with open(file_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

    def load(self, key: str) -> Any:
        """Load data from persistent storage"""
        try:
            file_path = os.path.join(self.storage_dir, f"{key}.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
        return None

    def clear(self, key: str = None) -> None:
        """Clear persistent storage for a key or all keys"""
        try:
            if key:
                file_path = os.path.join(self.storage_dir, f"{key}.json")
                if os.path.exists(file_path):
                    os.remove(file_path)
            else:
                for file_name in os.listdir(self.storage_dir):
                    if file_name.endswith(".json"):
                        os.remove(os.path.join(self.storage_dir, file_name))
                logger.info("Cleared all cache")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
