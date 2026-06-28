"""
Nexus AI — Configuration Settings
Pydantic-based settings with environment variable support.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- App ---
    app_name: str = "Nexus AI"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    cors_origins: list[str] = ["http://localhost:3000", "https://*.vercel.app"]

    # --- Supabase ---
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_anon_key: str = Field(..., description="Supabase anon/public key")
    supabase_service_role_key: str = Field(..., description="Supabase service role key (server-side)")
    supabase_jwt_secret: str = Field(..., description="Supabase JWT secret for token verification")

    # --- Default LLM (Developer's key for free trial chats) ---
    default_llm_provider: str = Field(default="gemini", description="Default LLM provider for trial chats")
    default_llm_api_key: str = Field(..., description="Developer's API key for trial chats")
    free_chat_limit: int = Field(default=4, description="Number of free chats before requiring user API key")

    # --- Embeddings (Server-side, always Gemini) ---
    gemini_embedding_api_key: str = Field(..., description="Gemini API key for embeddings (server-side)")
    embedding_model: str = "gemini-embedding-001"
    embedding_dimensions: int = 768

    # --- Memory ---
    personal_memory_limit: int = 5
    collective_knowledge_limit: int = 3
    memory_recency_decay: float = 0.95

    # --- Encryption ---
    encryption_key: str = Field(..., description="Fernet key for encrypting user API keys")

    # --- Agent Config ---
    main_model_temperature: float = 0.7
    main_model_max_tokens: int = 4096
    fast_model_temperature: float = 0.3
    fast_model_max_tokens: int = 1024

    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore", # Fixes pydantic ValidationError for custom vars
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
