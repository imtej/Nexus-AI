"""
Nexus AI — Supabase Client Service
Handles all database operations via Supabase.
"""

import structlog
from supabase import create_client, Client
from app.config.settings import get_settings

logger = structlog.get_logger()

_supabase_client: Client | None = None
_supabase_admin_client: Client | None = None


def get_supabase_client() -> Client:
    """Get Supabase client with anon key (respects RLS)."""
    global _supabase_client
    if _supabase_client is None:
        settings = get_settings()
        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key,
        )
        logger.info("supabase_client_initialized", url=settings.supabase_url)
    return _supabase_client


def get_supabase_admin() -> Client:
    """Get Supabase client with service role key (bypasses RLS)."""
    global _supabase_admin_client
    if _supabase_admin_client is None:
        settings = get_settings()
        _supabase_admin_client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
        )
        logger.info("supabase_admin_client_initialized")
    return _supabase_admin_client
