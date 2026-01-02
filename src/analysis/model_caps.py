class ModelCapabilities:
    """
    Helper to return the context window size (in tokens) for known models.
    Defaults to 128000 if unknown (safe for most modern models).
    """
    
    # Known limits (approximate safe values)
    LIMITS = {
        # OpenAI
        "gpt-4o": 128000,
        "gpt-4o-mini": 128000,
        "gpt-4-turbo": 128000,
        "gpt-4": 8192,
        "gpt-3.5-turbo": 16385,
        "o1-": 128000,
        
        # Anthropic
        "claude-3-5-sonnet": 200000,
        "claude-3-opus": 200000,
        "claude-3-sonnet": 200000,
        "claude-3-haiku": 200000,
        
        # Google
        "gemini-1.5-pro": 1000000,
        "gemini-1.5-flash": 1000000,
        "gemini-pro": 32768,
        
        # Groq
        "llama-3.1-405b": 128000,
        "llama-3.1-70b": 128000,
        "llama-3.1-8b": 128000,
        "llama3-70b-8192": 8192,
        "llama3-8b-8192": 8192,
        "mixtral-8x7b-32768": 32768,
        "gemma-7b-it": 8192,
        "gemma2-9b-it": 8192,
        
        # DeepSeek
        "deepseek-coder": 32000,
        "deepseek-chat": 32000,
        
        # OpenRouter
        "openrouter": 128000,
        
        # Generic Local (Safe default for 8GB VRAM)
        "local-model": 8192 
    }

    @staticmethod
    def get_max_tokens(model_name: str) -> int:
        # Normalize
        name = model_name.lower()
        
        # Check explicit mapping
        for key, limit in ModelCapabilities.LIMITS.items():
            if key in name:
                return limit
        
        # Heuristic fallbacks
        if "gpt-4o" in name: return 128000
        if "gpt-4" in name: return 128000
        if "claude-3" in name: return 200000
        if "gemini-1.5" in name: return 1000000
        if "gemini" in name: return 32768
        if "llama-3.1" in name: return 128000
        if "llama-3" in name: return 8192
        if "128k" in name: return 128000
        if "32k" in name: return 32000
        if "16k" in name: return 16000
        if "8k" in name: return 8192
        
        # Default for unknown models - assume it's modern
        return 128000
