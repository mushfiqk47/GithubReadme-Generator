from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from src.core.config import config

class LLMFactory:
    """
    Factory to create LLM instances based on the active provider and configuration.
    """
    
    @staticmethod
    def get_model(model_name: str, temperature: float = 0.0) -> BaseChatModel:
        provider = config.ACTIVE_PROVIDER
        
        # Override for Local
        if config.is_local:
            return ChatOpenAI(
                base_url=config.LOCAL_LLM_BASE_URL,
                api_key="lm-studio",
                model=config.LOCAL_LLM_MODEL,
                temperature=temperature
            )

        # Provider Logic
        if provider == "openai":
            key = config.OPENAI_API_KEY.get_secret_value() if config.OPENAI_API_KEY else os.getenv("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY is missing. Please set it in Settings.")
            return ChatOpenAI(
                model=model_name, 
                api_key=key,
                temperature=temperature,
                max_retries=3
            )
            
        elif provider == "anthropic":
            key = config.ANTHROPIC_API_KEY.get_secret_value() if config.ANTHROPIC_API_KEY else os.getenv("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError("ANTHROPIC_API_KEY is missing. Please set it in Settings.")
            return ChatAnthropic(
                model=model_name, 
                api_key=key,
                temperature=temperature,
                max_retries=3
            )
            
        elif provider == "google":
            key = config.GOOGLE_API_KEY.get_secret_value() if config.GOOGLE_API_KEY else os.getenv("GOOGLE_API_KEY")
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
            key = config.GROQ_API_KEY.get_secret_value() if config.GROQ_API_KEY else os.getenv("GROQ_API_KEY")
            if not key:
                raise ValueError("GROQ_API_KEY is missing. Please set it in Settings.")
            return ChatGroq(
                model_name=model_name, 
                api_key=key,
                temperature=temperature,
                max_retries=3
            )
            
        elif provider == "openrouter":
            key = config.OPENROUTER_API_KEY.get_secret_value() if config.OPENROUTER_API_KEY else os.getenv("OPENROUTER_API_KEY")
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
