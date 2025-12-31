from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
import os

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Intelligent README Generator"
    VERSION: str = "0.2.1"
    
    # Active Provider (openai, anthropic, google, groq, openrouter, local)
    ACTIVE_PROVIDER: Literal["openai", "anthropic", "google", "groq", "openrouter", "local"] = Field(
        default="openai",
        description="The active LLM provider to use."
    )
    
    # API Keys (Optional so they can be set in UI if missing)
    GITHUB_TOKEN: Optional[SecretStr] = Field(default=None, description="GitHub Personal Access Token")
    OPENAI_API_KEY: Optional[SecretStr] = None
    ANTHROPIC_API_KEY: Optional[SecretStr] = None
    GOOGLE_API_KEY: Optional[SecretStr] = None
    GROQ_API_KEY: Optional[SecretStr] = None
    OPENROUTER_API_KEY: Optional[SecretStr] = None
    
    # Local Settings
    USE_LOCAL_LLM: bool = False
    LOCAL_LLM_BASE_URL: str = "http://localhost:1234/v1"
    LOCAL_LLM_MODEL: str = "local-model"
    
    # Model Selection (Defaults)
    MODEL_PLANNER: str = "gpt-4o"
    MODEL_WRITER: str = "gpt-4o"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Allow extra env vars
    )

    @property
    def is_local(self) -> bool:
        return self.ACTIVE_PROVIDER == "local"

# Singleton instance
config = Settings()
