import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class UserMemory:
    """
    Manages persistent user memory and preferences for the LLM agents.
    Mimics the behavior of llm-user-memory but safe for Windows.
    """

    def __init__(self, app_name: str = "github_readme_generator", auto_update: bool = True):
        self.app_name = app_name
        self.auto_update = auto_update
        self.memory_dir = Path.home() / ".config" / "llm-user-memory"
        self.memory_file = self.memory_dir / f"{app_name}.json"
        self._ensure_storage()

    def _ensure_storage(self):
        """Ensure the storage directory and file exist."""
        try:
            self.memory_dir.mkdir(parents=True, exist_ok=True)
            if not self.memory_file.exists():
                self._save_memory({})
        except Exception as e:
            logger.error(f"Failed to initialize memory storage: {e}")

    def _load_memory(self) -> Dict[str, Any]:
        """Load raw memory dict."""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
        return {}

    def _save_memory(self, data: Dict[str, Any]):
        """Save raw memory dict."""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")

    def load(self) -> str:
        """
        Returns a formatted string of the user's memory context 
        for injection into LLM prompts.
        """
        data = self._load_memory()
        if not data:
            return "No previous user preferences found."
        
        # Format the memory into a readable context
        context_lines = []
        for key, value in data.items():
            formatted_key = key.replace("_", " ").title()
            context_lines.append(f"- **{formatted_key}**: {value}")
        
        return "\n".join(context_lines)

    def update(self, new_data: Dict[str, Any]):
        """
        Updates the memory with new key-value pairs.
        Merges with existing data.
        """
        current_data = self._load_memory()
        current_data.update(new_data)
        self._save_memory(current_data)
        logger.info(f"Memory updated with keys: {list(new_data.keys())}")

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a specific memory item."""
        data = self._load_memory()
        return data.get(key, default)

# Global instance
memory = UserMemory()
