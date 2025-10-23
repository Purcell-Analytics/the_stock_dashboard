import os
import reflex as rx
from supabase import create_client, Client
import logging

supabase_client: Client | None = None
try:
    url: str | None = os.environ.get("SUPABASE_URL")
    key: str | None = os.environ.get("SUPABASE_KEY")
    if url and key:
        supabase_client = create_client(url, key)
    else:
        logging.warning(
            "Supabase URL or Key not found. Supabase client not initialized."
        )
except Exception as e:
    logging.exception(f"Supabase connection error: {e}")
    supabase_client = None


def get_supabase_client() -> Client | None:
    return supabase_client