"""
Optimized LLM factory with connection pooling and caching.
"""
import os
from typing import Optional, Dict
from functools import lru_cache
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from src.core.config import config


class LLMFactory:
    """
    Optimized factory to create LLM instances with caching.
    Reduces overhead by caching model instances.
    """
    
    # Cache for model instances (key: f"{provider}_{model_name}_{temperature}")
    _model_cache: Dict[str, BaseChatModel] = {}
    
    @classmethod
    def _get_cache_key(cls, provider: str, model_name: str, temperature: float) -> str:
        """Generate cache key for model instance."""
        return f"{provider}_{model_name}_{temperature}"
    
    @classmethod
    def get_model(cls, model_name: str, temperature: float = 0.0) -> BaseChatModel:
        """
        Get or create a cached LLM instance.
        
        Args:
            model_name: Name of the model
            temperature: Sampling temperature
        
        Returns:
            Cached or new LLM instance
        """
        provider = config.ACTIVE_PROVIDER
        cache_key = cls._get_cache_key(provider, model_name, temperature)
        
        # Check cache first
        if cache_key in cls._model_cache:
            return cls._model_cache[cache_key]
        
        # Create new instance
        model = cls._create_model(provider, model_name, temperature)
        
        # Cache it
        cls._model_cache[cache_key] = model
        return model
    
    @classmethod
    def _create_model(cls, provider: str, model_name: str, temperature: float) -> BaseChatModel:
        """Create a new LLM instance based on provider."""
        
        # Local LLM override
        if config.is_local:
            return ChatOpenAI(
                base_url=config.LOCAL_LLM_BASE_URL,
                api_key="lm-studio",
                model=config.LOCAL_LLM_MODEL,
                temperature=temperature
            )

        # Provider-specific creation
        if provider == "openai":
            key = cls._get_api_key("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY is missing. Please set it in Settings.")
            return ChatOpenAI(
                model=model_name, 
                api_key=key,
                temperature=temperature,
                max_retries=3
            )
            
        elif provider == "anthropic":
            key = cls._get_api_key("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError("ANTHROPIC_API_KEY is missing. Please set it in Settings.")
            return ChatAnthropic(
                model=model_name, 
                api_key=key,
                temperature=temperature,
                max_retries=3
            )
            
        elif provider == "google":
            key = cls._get_api_key("GOOGLE_API_KEY")
            if not key:
                raise ValueError("GOOGLE_API_KEY is missing. Please set it in Settings.")
            return ChatGoogleGenerativeAI(
                model=model_name, 
                google_api_key=key,
                temperature=temperature,
                convert_system_message_to_human=True,
                max_retries=3
            )
            
        elif provider == "groq":
            key = cls._get_api_key("GROQ_API_KEY")
            if not key:
                raise ValueError("GROQ_API_KEY is missing. Please set it in Settings.")
            return ChatGroq(
                model_name=model_name, 
                api_key=key,
                temperature=temperature,
                max_retries=3
            )
            
        elif provider == "openrouter":
            key = cls._get_api_key("OPENROUTER_API_KEY")
            if not key:
                raise ValueError("OPENROUTER_API_KEY is missing. Please set it in Settings.")
            return ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=key,
                model=model_name,
                temperature=temperature,
                max_retries=3,
                default_headers={
                    "HTTP-Referer": "https://github.com/mushfiqk47/intelligent-readme-generator",
                    "X-Title": "Intelligent README Generator"
                }
            )
            
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @classmethod
    def _get_api_key(cls, env_var: str) -> Optional[str]:
        """
        Safely get API key from config or environment.
        
        Args:
            env_var: Environment variable name
        
        Returns:
            API key or None
        """
        # Try pydantic config first
        config_value = getattr(config, env_var, None)
        if config_value:
            try:
                return config_value.get_secret_value()
            except AttributeError:
                return str(config_value)
        
        # Fallback to environment
        return os.getenv(env_var)
    
    @classmethod
    def clear_cache(cls):
        """Clear the model cache. Useful for testing or configuration changes."""
        cls._model_cache.clear()
    
    @classmethod
    def get_cache_size(cls) -> int:
        """Get current cache size for monitoring."""
        return len(cls._model_cache)
