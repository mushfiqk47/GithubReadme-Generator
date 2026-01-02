"""
Shared token counting utilities.
"""
import tiktoken
from typing import Optional


class TokenCounter:
    """Centralized token counting with caching."""
    
    def __init__(self, encoding: str = "cl100k_base"):
        self._encoding_name = encoding
        self._encoder: Optional[tiktoken.Encoding] = None
        self._load_encoder()
    
    def _load_encoder(self):
        """Load tiktoken encoder with fallback."""
        try:
            self._encoder = tiktoken.get_encoding(self._encoding_name)
        except Exception:
            self._encoder = None
    
    def count(self, text: str) -> int:
        """Count tokens in text with fallback."""
        if not text:
            return 0
        if self._encoder:
            try:
                return len(self._encoder.encode(text, disallowed_special=()))
            except Exception:
                pass
        # Fallback: approximate 1 token = 4 characters
        return len(text) // 4
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token budget."""
        if not text or max_tokens <= 0:
            return ""
        
        if self._encoder:
            try:
                tokens = self._encoder.encode(text, disallowed_special=())
                if len(tokens) <= max_tokens:
                    return text
                truncated_tokens = tokens[:max_tokens]
                return self._encoder.decode(truncated_tokens)
            except Exception:
                pass
        
        # Fallback: character-based truncation
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n... [TRUNCATED]"


# Singleton instance
_default_counter = TokenCounter()


def count_tokens(text: str) -> int:
    """Quick token count using default encoder."""
    return _default_counter.count(text)


def truncate_tokens(text: str, max_tokens: int) -> str:
    """Quick truncation using default encoder."""
    return _default_counter.truncate_to_tokens(text, max_tokens)
